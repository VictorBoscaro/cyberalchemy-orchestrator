package rwosidecar

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"sync"
)

const (
	// DurableStoreFormatV1 is the only store format understood by this local
	// candidate. Format changes must use a new value rather than reinterpret
	// existing bytes.
	DurableStoreFormatV1 = "RWO_DURABLE_STORE_V1"

	durableHeaderVersion uint16 = 1
	durableFrameVersion  uint16 = 1
	maxHeaderBodyBytes          = 1 << 20
	maxRecordBodyBytes          = 16 << 20
)

var (
	durableHeaderMagic = [8]byte{'R', 'W', 'O', 'H', 'D', 'R', '0', '1'}
	durableFrameMagic  = [8]byte{'R', 'W', 'O', 'L', 'O', 'G', '0', '1'}

	// ErrDurableStoreLocked means another live process or store instance owns
	// the exclusive advisory lock.
	ErrDurableStoreLocked = errors.New("RWO durable store is locked")
	// ErrDurableStoreLockUnsupported means the host cannot provide the
	// candidate's required advisory-lock behavior.
	ErrDurableStoreLockUnsupported = errors.New("RWO durable store locking is unsupported")
	// ErrDurableStoreHeader means the canonical header is incomplete, malformed,
	// or does not match the requested graph/version binding.
	ErrDurableStoreHeader = errors.New("invalid RWO durable store header")
	// ErrDurableStoreCorrupt means a complete frame or verified projection is
	// inconsistent. Only an incomplete terminal tail is repairable.
	ErrDurableStoreCorrupt = errors.New("corrupt RWO durable store")
	// ErrDurableStoreExpectation means an append compare-and-swap did not match
	// the current verified prefix or cursor projection.
	ErrDurableStoreExpectation = errors.New("RWO durable store expectation mismatch")
	// ErrDurableStoreNeedsReopen means an append write or Sync became uncertain.
	// The live descriptor is quarantined and no operation may publish state.
	ErrDurableStoreNeedsReopen = errors.New("RWO durable store needs verified reopen")
	// ErrDurableStoreClosed means the store was explicitly closed.
	ErrDurableStoreClosed = errors.New("RWO durable store is closed")
)

var zeroFrameSHA256 = strings.Repeat("0", sha256.Size*2)

// EmptyCursorSHA256 is the exact digest used for a stream which has no
// committed cursor yet.
var EmptyCursorSHA256 = digestHex(nil)

// DurableStoreHeader binds one file to one compiled graph and semantic tuple.
// RawCompositionSHA256 is the digest of the exact opaque composition bytes.
type DurableStoreHeader struct {
	StoreFormat          string       `json:"store_format"`
	GraphIdentity        string       `json:"graph_identity"`
	RawCompositionSHA256 string       `json:"raw_composition_sha256"`
	Tuple                VersionTuple `json:"tuple"`
	StoreInstanceID      string       `json:"store_instance_id"`
}

// StoreHeader is a short compatibility name for DurableStoreHeader.
type StoreHeader = DurableStoreHeader

func (header DurableStoreHeader) validate() error {
	if header.StoreFormat != DurableStoreFormatV1 {
		return fmt.Errorf("%w: store_format must be %q", ErrDurableStoreHeader, DurableStoreFormatV1)
	}
	if header.GraphIdentity == "" || header.StoreInstanceID == "" {
		return fmt.Errorf("%w: graph_identity and store_instance_id are required", ErrDurableStoreHeader)
	}
	if err := validateDigest(header.RawCompositionSHA256); err != nil {
		return fmt.Errorf("%w: raw composition digest: %v", ErrDurableStoreHeader, err)
	}
	if err := header.Tuple.validate(); err != nil {
		return fmt.Errorf("%w: %v", ErrDurableStoreHeader, err)
	}
	return nil
}

// DurableRecordType is the closed on-disk numeric discriminator. Individual
// layers own named constants; zero is always invalid.
type DurableRecordType uint16

// DurableRecord prevents arbitrary map-shaped values from crossing the store
// boundary. Later layers define closed structs which implement this method.
type DurableRecord interface {
	DurableRecordType() DurableRecordType
}

// CursorTransition gives the store enough closed metadata to compare and
// rebuild a semantic cursor projection without interpreting opaque cursor
// bytes. All digests are lowercase hexadecimal SHA-256 strings.
type CursorTransition struct {
	StreamKey              string `json:"stream_key"`
	ExpectedPreviousSHA256 string `json:"expected_previous_sha256"`
	NextSHA256             string `json:"next_sha256"`
}

func (transition *CursorTransition) validate() error {
	if transition == nil {
		return nil
	}
	if transition.StreamKey == "" {
		return fmt.Errorf("%w: cursor stream key is required", ErrDurableStoreExpectation)
	}
	if err := validateDigest(transition.ExpectedPreviousSHA256); err != nil {
		return fmt.Errorf("%w: previous cursor digest: %v", ErrDurableStoreExpectation, err)
	}
	if err := validateDigest(transition.NextSHA256); err != nil {
		return fmt.Errorf("%w: next cursor digest: %v", ErrDurableStoreExpectation, err)
	}
	return nil
}

// AppendExpectation is an exact compare-and-swap over the verified log tip and,
// for semantic commits, one cursor projection.
type AppendExpectation struct {
	ExpectedSequence            uint64
	ExpectedPreviousFrameSHA256 string
	Cursor                      *CursorTransition
}

// DurableRecordRef is returned only after the complete frame has been written
// and Sync has succeeded.
type DurableRecordRef struct {
	Sequence    uint64
	Offset      int64
	FrameSHA256 string
}

// StoredDurableRecord is a defensive copy of one verified frame body. Body is
// the exact JSON encoding produced for the original closed record struct.
type StoredDurableRecord struct {
	Type   DurableRecordType
	Body   []byte
	Cursor *CursorTransition
	Ref    DurableRecordRef
}

// DurableStoreSnapshot is a defensive view of the verified in-memory
// projections. The map is host projection data, never a semantic record body.
type DurableStoreSnapshot struct {
	Header                  DurableStoreHeader
	LastSequence            uint64
	LastFrameSHA256         string
	Records                 []StoredDurableRecord
	CursorSHA256ByStreamKey map[string]string
}

// DurableStoreFailureHooks are deterministic injection points for crash tests.
// They apply only to record appends, never header creation or recovery repair.
// Returning an error after a partial write intentionally poisons the store.
type DurableStoreFailureHooks struct {
	WriteFrame func(*os.File, []byte) (int, error)
	SyncFrame  func(*os.File) error
}

type durableStoreOptions struct {
	failureHooks DurableStoreFailureHooks
}

// DurableStoreOption configures a store open without changing persisted
// semantics.
type DurableStoreOption func(*durableStoreOptions)

// WithDurableStoreFailureHooks installs append-only test injection hooks.
func WithDurableStoreFailureHooks(hooks DurableStoreFailureHooks) DurableStoreOption {
	return func(options *durableStoreOptions) {
		options.failureHooks = hooks
	}
}

type persistedRecordEnvelope struct {
	BodyBase64 string            `json:"body_base64"`
	Cursor     *CursorTransition `json:"cursor,omitempty"`
}

// DurableStore is the single owner of one verified append-only file.
type DurableStore struct {
	mu sync.Mutex

	path          string
	file          *os.File
	header        DurableStoreHeader
	headerEnd     int64
	lastSequence  uint64
	lastFrameHash [sha256.Size]byte
	records       []StoredDurableRecord
	cursorDigests map[string]string
	options       durableStoreOptions
	poisoned      bool
	closed        bool
}

// OpenDurableStore creates a new atomically-headered file when absent or opens
// and verifies the exact existing binding. It repairs only an incomplete final
// frame and obtains an exclusive nonblocking advisory lock.
func OpenDurableStore(path string, expected DurableStoreHeader, options ...DurableStoreOption) (*DurableStore, error) {
	if path == "" {
		return nil, fmt.Errorf("%w: path is required", ErrDurableStoreHeader)
	}
	if err := expected.validate(); err != nil {
		return nil, err
	}
	configuration := durableStoreOptions{}
	for _, option := range options {
		if option != nil {
			option(&configuration)
		}
	}
	if err := ensureDurableStoreFile(path, expected); err != nil {
		return nil, err
	}
	file, err := os.OpenFile(path, os.O_RDWR, 0)
	if err != nil {
		return nil, fmt.Errorf("open durable store: %w", err)
	}
	if err := lockStoreFile(file); err != nil {
		_ = file.Close()
		return nil, err
	}
	store := &DurableStore{
		path:          path,
		file:          file,
		header:        expected,
		cursorDigests: make(map[string]string),
		options:       configuration,
	}
	if err := store.recover(expected); err != nil {
		_ = unlockStoreFile(file)
		_ = file.Close()
		return nil, err
	}
	return store, nil
}

// NewDurableStore is an alias for OpenDurableStore: creation and reopen share
// the same verified binding path.
func NewDurableStore(path string, expected DurableStoreHeader, options ...DurableStoreOption) (*DurableStore, error) {
	return OpenDurableStore(path, expected, options...)
}

// Append writes and syncs one exact frame before publishing any projection.
func (store *DurableStore) Append(expectation AppendExpectation, record DurableRecord) (DurableRecordRef, error) {
	if store == nil {
		return DurableRecordRef{}, ErrDurableStoreClosed
	}
	store.mu.Lock()
	defer store.mu.Unlock()
	if err := store.operableLocked(); err != nil {
		return DurableRecordRef{}, err
	}
	if record == nil || (reflect.ValueOf(record).Kind() == reflect.Ptr && reflect.ValueOf(record).IsNil()) {
		return DurableRecordRef{}, fmt.Errorf("%w: record is required", ErrDurableStoreExpectation)
	}
	recordType := record.DurableRecordType()
	if recordType == 0 {
		return DurableRecordRef{}, fmt.Errorf("%w: record type zero is invalid", ErrDurableStoreExpectation)
	}
	nextSequence := store.lastSequence + 1
	if expectation.ExpectedSequence != nextSequence {
		return DurableRecordRef{}, fmt.Errorf("%w: expected sequence %d, current next %d", ErrDurableStoreExpectation, expectation.ExpectedSequence, nextSequence)
	}
	expectedPreviousHash, err := parseDigest(expectation.ExpectedPreviousFrameSHA256)
	if err != nil || expectedPreviousHash != store.lastFrameHash {
		return DurableRecordRef{}, fmt.Errorf("%w: previous frame hash", ErrDurableStoreExpectation)
	}
	if err := expectation.Cursor.validate(); err != nil {
		return DurableRecordRef{}, err
	}
	if expectation.Cursor != nil {
		current := store.cursorDigestLocked(expectation.Cursor.StreamKey)
		if expectation.Cursor.ExpectedPreviousSHA256 != current {
			return DurableRecordRef{}, fmt.Errorf("%w: cursor for stream %q", ErrDurableStoreExpectation, expectation.Cursor.StreamKey)
		}
	}
	body, err := json.Marshal(record)
	if err != nil {
		return DurableRecordRef{}, fmt.Errorf("marshal durable record: %w", err)
	}
	if len(body) == 0 || len(body) > maxRecordBodyBytes {
		return DurableRecordRef{}, fmt.Errorf("%w: record body size %d", ErrDurableStoreExpectation, len(body))
	}
	envelopeBytes, err := json.Marshal(persistedRecordEnvelope{
		BodyBase64: base64.StdEncoding.EncodeToString(body),
		Cursor:     cloneCursorTransition(expectation.Cursor),
	})
	if err != nil {
		return DurableRecordRef{}, fmt.Errorf("marshal durable record envelope: %w", err)
	}
	if len(envelopeBytes) > maxRecordBodyBytes {
		return DurableRecordRef{}, fmt.Errorf("%w: persisted record body size %d", ErrDurableStoreExpectation, len(envelopeBytes))
	}
	frame, frameHash := encodeDurableFrame(recordType, nextSequence, store.lastFrameHash, envelopeBytes)
	offset, err := store.file.Seek(0, io.SeekEnd)
	if err != nil {
		store.poisonLocked()
		return DurableRecordRef{}, fmt.Errorf("%w: seek append: %w", ErrDurableStoreNeedsReopen, err)
	}
	if err := store.writeFrameLocked(frame); err != nil {
		store.poisonLocked()
		return DurableRecordRef{}, fmt.Errorf("%w: append frame: %w", ErrDurableStoreNeedsReopen, err)
	}
	if err := store.syncFrameLocked(); err != nil {
		store.poisonLocked()
		return DurableRecordRef{}, fmt.Errorf("%w: sync frame: %w", ErrDurableStoreNeedsReopen, err)
	}
	ref := DurableRecordRef{
		Sequence:    nextSequence,
		Offset:      offset,
		FrameSHA256: hex.EncodeToString(frameHash[:]),
	}
	store.lastSequence = nextSequence
	store.lastFrameHash = frameHash
	if expectation.Cursor != nil {
		store.cursorDigests[expectation.Cursor.StreamKey] = expectation.Cursor.NextSHA256
	}
	store.records = append(store.records, StoredDurableRecord{
		Type:   recordType,
		Body:   cloneBytes(body),
		Cursor: cloneCursorTransition(expectation.Cursor),
		Ref:    ref,
	})
	return ref, nil
}

// Tip returns the current verified CAS values.
func (store *DurableStore) Tip() (nextSequence uint64, previousFrameSHA256 string, err error) {
	if store == nil {
		return 0, "", ErrDurableStoreClosed
	}
	store.mu.Lock()
	defer store.mu.Unlock()
	if err := store.operableLocked(); err != nil {
		return 0, "", err
	}
	return store.lastSequence + 1, hex.EncodeToString(store.lastFrameHash[:]), nil
}

// CursorSHA256 returns the verified cursor projection or EmptyCursorSHA256 when
// the stream has no commit.
func (store *DurableStore) CursorSHA256(streamKey string) (string, error) {
	if store == nil {
		return "", ErrDurableStoreClosed
	}
	store.mu.Lock()
	defer store.mu.Unlock()
	if err := store.operableLocked(); err != nil {
		return "", err
	}
	if streamKey == "" {
		return "", fmt.Errorf("%w: cursor stream key is required", ErrDurableStoreExpectation)
	}
	return store.cursorDigestLocked(streamKey), nil
}

// Snapshot returns only copies of the verified prefix and projections.
func (store *DurableStore) Snapshot() (DurableStoreSnapshot, error) {
	if store == nil {
		return DurableStoreSnapshot{}, ErrDurableStoreClosed
	}
	store.mu.Lock()
	defer store.mu.Unlock()
	if err := store.operableLocked(); err != nil {
		return DurableStoreSnapshot{}, err
	}
	return DurableStoreSnapshot{
		Header:                  store.header,
		LastSequence:            store.lastSequence,
		LastFrameSHA256:         hex.EncodeToString(store.lastFrameHash[:]),
		Records:                 cloneStoredRecords(store.records),
		CursorSHA256ByStreamKey: cloneStringMap(store.cursorDigests),
	}, nil
}

// Close releases the exclusive lock. A poisoned store remains classified as
// needs_reopen even though its descriptor was already quarantined.
func (store *DurableStore) Close() error {
	if store == nil {
		return nil
	}
	store.mu.Lock()
	defer store.mu.Unlock()
	if store.closed {
		return nil
	}
	store.closed = true
	if store.file == nil {
		return nil
	}
	unlockErr := unlockStoreFile(store.file)
	closeErr := store.file.Close()
	store.file = nil
	return errors.Join(unlockErr, closeErr)
}

func (store *DurableStore) operableLocked() error {
	if store.poisoned {
		return ErrDurableStoreNeedsReopen
	}
	if store.closed || store.file == nil {
		return ErrDurableStoreClosed
	}
	return nil
}

func (store *DurableStore) cursorDigestLocked(streamKey string) string {
	if digest := store.cursorDigests[streamKey]; digest != "" {
		return digest
	}
	return EmptyCursorSHA256
}

func (store *DurableStore) poisonLocked() {
	store.poisoned = true
	if store.file == nil {
		return
	}
	_ = unlockStoreFile(store.file)
	_ = store.file.Close()
	store.file = nil
}

func (store *DurableStore) writeFrameLocked(frame []byte) error {
	written := 0
	for written < len(frame) {
		var count int
		var err error
		if store.options.failureHooks.WriteFrame != nil {
			count, err = store.options.failureHooks.WriteFrame(store.file, frame[written:])
		} else {
			count, err = store.file.Write(frame[written:])
		}
		if count < 0 || count > len(frame)-written {
			return fmt.Errorf("invalid write count %d", count)
		}
		written += count
		if err != nil {
			return err
		}
		if count == 0 {
			return io.ErrShortWrite
		}
	}
	return nil
}

func (store *DurableStore) syncFrameLocked() error {
	if store.options.failureHooks.SyncFrame != nil {
		return store.options.failureHooks.SyncFrame(store.file)
	}
	return store.file.Sync()
}

func (store *DurableStore) recover(expected DurableStoreHeader) error {
	header, headerEnd, err := readDurableHeader(store.file)
	if err != nil {
		return err
	}
	if header != expected {
		return fmt.Errorf("%w: requested binding differs from canonical header", ErrDurableStoreHeader)
	}
	store.header = header
	store.headerEnd = headerEnd
	info, err := store.file.Stat()
	if err != nil {
		return fmt.Errorf("stat durable store: %w", err)
	}
	lastGood := headerEnd
	for lastGood < info.Size() {
		remaining := info.Size() - lastGood
		if remaining < int64(durableFramePrefixSize()+sha256.Size) {
			return store.truncateIncompleteTail(lastGood)
		}
		prefix := make([]byte, durableFramePrefixSize())
		if _, err := store.file.ReadAt(prefix, lastGood); err != nil {
			return fmt.Errorf("%w: read frame prefix at %d: %v", ErrDurableStoreCorrupt, lastGood, err)
		}
		if !bytes.Equal(prefix[:len(durableFrameMagic)], durableFrameMagic[:]) {
			return fmt.Errorf("%w: frame magic at %d", ErrDurableStoreCorrupt, lastGood)
		}
		version := binary.BigEndian.Uint16(prefix[8:10])
		if version != durableFrameVersion {
			return fmt.Errorf("%w: frame version %d at %d", ErrDurableStoreCorrupt, version, lastGood)
		}
		recordType := DurableRecordType(binary.BigEndian.Uint16(prefix[10:12]))
		if recordType == 0 {
			return fmt.Errorf("%w: frame type zero at %d", ErrDurableStoreCorrupt, lastGood)
		}
		bodyLength := uint64(binary.BigEndian.Uint32(prefix[12:16]))
		if bodyLength == 0 || bodyLength > maxRecordBodyBytes {
			return fmt.Errorf("%w: frame body length %d at %d", ErrDurableStoreCorrupt, bodyLength, lastGood)
		}
		frameLength := int64(len(prefix)) + int64(bodyLength) + sha256.Size
		if remaining < frameLength {
			return store.truncateIncompleteTail(lastGood)
		}
		frame := make([]byte, frameLength)
		if _, err := store.file.ReadAt(frame, lastGood); err != nil {
			return fmt.Errorf("%w: read complete frame at %d: %v", ErrDurableStoreCorrupt, lastGood, err)
		}
		sequence := binary.BigEndian.Uint64(prefix[16:24])
		if sequence != store.lastSequence+1 {
			return fmt.Errorf("%w: sequence %d after %d", ErrDurableStoreCorrupt, sequence, store.lastSequence)
		}
		if !bytes.Equal(prefix[24:56], store.lastFrameHash[:]) {
			return fmt.Errorf("%w: previous hash at sequence %d", ErrDurableStoreCorrupt, sequence)
		}
		bodyStart := len(prefix)
		bodyEnd := bodyStart + int(bodyLength)
		body := frame[bodyStart:bodyEnd]
		bodyDigest := sha256.Sum256(body)
		if !bytes.Equal(prefix[56:88], bodyDigest[:]) {
			return fmt.Errorf("%w: body digest at sequence %d", ErrDurableStoreCorrupt, sequence)
		}
		frameDigest := sha256.Sum256(frame[:bodyEnd])
		if !bytes.Equal(frame[bodyEnd:], frameDigest[:]) {
			return fmt.Errorf("%w: frame digest at sequence %d", ErrDurableStoreCorrupt, sequence)
		}
		decodedBody, cursor, err := decodePersistedEnvelope(body)
		if err != nil {
			return fmt.Errorf("%w: record envelope at sequence %d: %v", ErrDurableStoreCorrupt, sequence, err)
		}
		if cursor != nil {
			if err := cursor.validate(); err != nil {
				return fmt.Errorf("%w: cursor transition at sequence %d: %v", ErrDurableStoreCorrupt, sequence, err)
			}
			current := store.cursorDigestLocked(cursor.StreamKey)
			if cursor.ExpectedPreviousSHA256 != current {
				return fmt.Errorf("%w: cursor chain at sequence %d", ErrDurableStoreCorrupt, sequence)
			}
			store.cursorDigests[cursor.StreamKey] = cursor.NextSHA256
		}
		ref := DurableRecordRef{
			Sequence:    sequence,
			Offset:      lastGood,
			FrameSHA256: hex.EncodeToString(frameDigest[:]),
		}
		store.records = append(store.records, StoredDurableRecord{
			Type:   recordType,
			Body:   decodedBody,
			Cursor: cursor,
			Ref:    ref,
		})
		store.lastSequence = sequence
		store.lastFrameHash = frameDigest
		lastGood += frameLength
	}
	_, err = store.file.Seek(0, io.SeekEnd)
	return err
}

func (store *DurableStore) truncateIncompleteTail(lastGood int64) error {
	if err := store.file.Truncate(lastGood); err != nil {
		return fmt.Errorf("truncate incomplete durable tail: %w", err)
	}
	if err := store.file.Sync(); err != nil {
		return fmt.Errorf("sync truncated durable tail: %w", err)
	}
	_, err := store.file.Seek(0, io.SeekEnd)
	return err
}

func ensureDurableStoreFile(path string, header DurableStoreHeader) error {
	if _, err := os.Stat(path); err == nil {
		return nil
	} else if !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("stat durable store: %w", err)
	}
	guardPath := path + ".create.lock"
	guard, err := os.OpenFile(guardPath, os.O_CREATE|os.O_RDWR, 0o600)
	if err != nil {
		return fmt.Errorf("open durable store creation guard: %w", err)
	}
	if err := lockStoreFile(guard); err != nil {
		_ = guard.Close()
		return err
	}
	defer func() {
		_ = unlockStoreFile(guard)
		_ = guard.Close()
	}()
	if _, err := os.Stat(path); err == nil {
		return nil
	} else if !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("stat durable store after creation lock: %w", err)
	}
	directory := filepath.Dir(path)
	temporary, err := os.CreateTemp(directory, "."+filepath.Base(path)+".header-")
	if err != nil {
		return fmt.Errorf("create durable store header candidate: %w", err)
	}
	temporaryPath := temporary.Name()
	removeTemporary := true
	defer func() {
		_ = temporary.Close()
		if removeTemporary {
			_ = os.Remove(temporaryPath)
		}
	}()
	if err := temporary.Chmod(0o600); err != nil {
		return fmt.Errorf("set durable store permissions: %w", err)
	}
	headerBytes, err := encodeDurableHeader(header)
	if err != nil {
		return err
	}
	if err := writeAll(temporary, headerBytes); err != nil {
		return fmt.Errorf("write durable store header: %w", err)
	}
	if err := temporary.Sync(); err != nil {
		return fmt.Errorf("sync durable store header: %w", err)
	}
	if err := temporary.Close(); err != nil {
		return fmt.Errorf("close durable store header: %w", err)
	}
	if err := os.Rename(temporaryPath, path); err != nil {
		return fmt.Errorf("install durable store header: %w", err)
	}
	removeTemporary = false
	if err := syncDirectory(directory); err != nil {
		return fmt.Errorf("sync durable store directory: %w", err)
	}
	return nil
}

func encodeDurableHeader(header DurableStoreHeader) ([]byte, error) {
	body, err := json.Marshal(header)
	if err != nil {
		return nil, fmt.Errorf("marshal durable store header: %w", err)
	}
	if len(body) == 0 || len(body) > maxHeaderBodyBytes {
		return nil, fmt.Errorf("%w: header body size %d", ErrDurableStoreHeader, len(body))
	}
	digest := sha256.Sum256(body)
	encoded := make([]byte, 8+2+4+sha256.Size+len(body))
	copy(encoded[:8], durableHeaderMagic[:])
	binary.BigEndian.PutUint16(encoded[8:10], durableHeaderVersion)
	binary.BigEndian.PutUint32(encoded[10:14], uint32(len(body)))
	copy(encoded[14:46], digest[:])
	copy(encoded[46:], body)
	return encoded, nil
}

func readDurableHeader(file *os.File) (DurableStoreHeader, int64, error) {
	fixed := make([]byte, 8+2+4+sha256.Size)
	if _, err := file.ReadAt(fixed, 0); err != nil {
		return DurableStoreHeader{}, 0, fmt.Errorf("%w: canonical header is incomplete: %v", ErrDurableStoreHeader, err)
	}
	if !bytes.Equal(fixed[:8], durableHeaderMagic[:]) {
		return DurableStoreHeader{}, 0, fmt.Errorf("%w: header magic", ErrDurableStoreHeader)
	}
	if version := binary.BigEndian.Uint16(fixed[8:10]); version != durableHeaderVersion {
		return DurableStoreHeader{}, 0, fmt.Errorf("%w: header version %d", ErrDurableStoreHeader, version)
	}
	bodyLength := binary.BigEndian.Uint32(fixed[10:14])
	if bodyLength == 0 || bodyLength > maxHeaderBodyBytes {
		return DurableStoreHeader{}, 0, fmt.Errorf("%w: header body length %d", ErrDurableStoreHeader, bodyLength)
	}
	body := make([]byte, bodyLength)
	if _, err := file.ReadAt(body, int64(len(fixed))); err != nil {
		return DurableStoreHeader{}, 0, fmt.Errorf("%w: canonical header body is incomplete: %v", ErrDurableStoreHeader, err)
	}
	digest := sha256.Sum256(body)
	if !bytes.Equal(fixed[14:46], digest[:]) {
		return DurableStoreHeader{}, 0, fmt.Errorf("%w: header digest", ErrDurableStoreHeader)
	}
	var header DurableStoreHeader
	if err := decodeClosedJSON(body, &header); err != nil {
		return DurableStoreHeader{}, 0, fmt.Errorf("%w: decode header: %v", ErrDurableStoreHeader, err)
	}
	if err := header.validate(); err != nil {
		return DurableStoreHeader{}, 0, err
	}
	return header, int64(len(fixed)) + int64(bodyLength), nil
}

func encodeDurableFrame(recordType DurableRecordType, sequence uint64, previousHash [sha256.Size]byte, body []byte) ([]byte, [sha256.Size]byte) {
	prefixLength := durableFramePrefixSize()
	frame := make([]byte, prefixLength+len(body)+sha256.Size)
	copy(frame[:8], durableFrameMagic[:])
	binary.BigEndian.PutUint16(frame[8:10], durableFrameVersion)
	binary.BigEndian.PutUint16(frame[10:12], uint16(recordType))
	binary.BigEndian.PutUint32(frame[12:16], uint32(len(body)))
	binary.BigEndian.PutUint64(frame[16:24], sequence)
	copy(frame[24:56], previousHash[:])
	bodyHash := sha256.Sum256(body)
	copy(frame[56:88], bodyHash[:])
	copy(frame[prefixLength:], body)
	frameHash := sha256.Sum256(frame[:prefixLength+len(body)])
	copy(frame[prefixLength+len(body):], frameHash[:])
	return frame, frameHash
}

func durableFramePrefixSize() int {
	return 8 + 2 + 2 + 4 + 8 + sha256.Size + sha256.Size
}

func decodePersistedEnvelope(encoded []byte) ([]byte, *CursorTransition, error) {
	var envelope persistedRecordEnvelope
	if err := decodeClosedJSON(encoded, &envelope); err != nil {
		return nil, nil, err
	}
	if envelope.BodyBase64 == "" {
		return nil, nil, errors.New("record body is required")
	}
	body, err := base64.StdEncoding.Strict().DecodeString(envelope.BodyBase64)
	if err != nil || len(body) == 0 || len(body) > maxRecordBodyBytes || !json.Valid(body) {
		return nil, nil, errors.New("record body is not valid bounded base64 JSON")
	}
	return body, cloneCursorTransition(envelope.Cursor), nil
}

func decodeClosedJSON(encoded []byte, destination any) error {
	decoder := json.NewDecoder(bytes.NewReader(encoded))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(destination); err != nil {
		return err
	}
	if decoder.More() {
		return errors.New("additional JSON value")
	}
	var trailing any
	if err := decoder.Decode(&trailing); !errors.Is(err, io.EOF) {
		if err == nil {
			return errors.New("additional JSON value")
		}
		return err
	}
	return nil
}

func writeAll(writer io.Writer, bytes []byte) error {
	for len(bytes) > 0 {
		count, err := writer.Write(bytes)
		if count < 0 || count > len(bytes) {
			return fmt.Errorf("invalid write count %d", count)
		}
		bytes = bytes[count:]
		if err != nil {
			return err
		}
		if count == 0 {
			return io.ErrShortWrite
		}
	}
	return nil
}

func syncDirectory(path string) error {
	directory, err := os.Open(path)
	if err != nil {
		return err
	}
	defer directory.Close()
	return directory.Sync()
}

func parseDigest(value string) ([sha256.Size]byte, error) {
	var parsed [sha256.Size]byte
	if err := validateDigest(value); err != nil {
		return parsed, err
	}
	decoded, _ := hex.DecodeString(value)
	copy(parsed[:], decoded)
	return parsed, nil
}

func validateDigest(value string) error {
	if len(value) != sha256.Size*2 || strings.ToLower(value) != value {
		return errors.New("lowercase SHA-256 hex required")
	}
	decoded, err := hex.DecodeString(value)
	if err != nil || len(decoded) != sha256.Size {
		return errors.New("lowercase SHA-256 hex required")
	}
	return nil
}

func digestHex(value []byte) string {
	digest := sha256.Sum256(value)
	return hex.EncodeToString(digest[:])
}

func cloneCursorTransition(value *CursorTransition) *CursorTransition {
	if value == nil {
		return nil
	}
	copy := *value
	return &copy
}

func cloneStoredRecords(records []StoredDurableRecord) []StoredDurableRecord {
	copyRecords := make([]StoredDurableRecord, len(records))
	for index, record := range records {
		copyRecords[index] = record
		copyRecords[index].Body = cloneBytes(record.Body)
		copyRecords[index].Cursor = cloneCursorTransition(record.Cursor)
	}
	return copyRecords
}

func cloneStringMap(values map[string]string) map[string]string {
	copyValues := make(map[string]string, len(values))
	for key, value := range values {
		copyValues[key] = value
	}
	return copyValues
}
