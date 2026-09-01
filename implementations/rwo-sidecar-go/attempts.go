package rwosidecar

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"sort"
	"strconv"
	"sync"
	"time"
)

const RecordTypeAttemptJournalV1 DurableRecordType = 0x0301

const (
	AttemptPrepared        AttemptState = "prepared"
	AttemptSendArmed       AttemptState = "send_armed"
	AttemptKnownNotSent    AttemptState = "known_not_sent"
	AttemptDeliveryUnknown AttemptState = "delivery_unknown"
	AttemptSessionKnown    AttemptState = "session_known"
	AttemptStreamAttached  AttemptState = "stream_attached"
	AttemptCancelRequested AttemptState = "cancel_requested"
	AttemptBlocked         AttemptState = "blocked"
	AttemptAcknowledged    AttemptState = "acknowledged"
)

const (
	attemptTransitionPrepared            = "attempt_prepared"
	attemptTransitionLeaseClaimed        = "lease_claimed"
	attemptTransitionSendArmed           = "send_armed"
	attemptTransitionKnownNotSent        = "known_not_sent"
	attemptTransitionSendTryAllocated    = "send_try_allocated"
	attemptTransitionDeliveryUnknown     = "delivery_unknown"
	attemptTransitionSessionKnown        = "session_known"
	attemptTransitionStreamAttached      = "stream_attached"
	attemptTransitionStreamDetached      = "stream_detached"
	attemptTransitionCancelRequested     = "cancel_requested"
	attemptTransitionBlocked             = "attempt_blocked"
	attemptTransitionAcknowledged        = "attempt_acknowledged"
	attemptTransitionUncorrelatedSession = "uncorrelated_session"
)

var (
	ErrAttemptInvalid         = errors.New("invalid RWO physical attempt")
	ErrAttemptNotFound        = errors.New("RWO physical attempt not found")
	ErrAttemptConflict        = errors.New("RWO physical attempt conflicts with durable state")
	ErrAttemptTransition      = errors.New("RWO physical attempt transition is forbidden")
	ErrAttemptLeaseHeld       = errors.New("RWO physical attempt lease is held")
	ErrAttemptStaleFence      = errors.New("RWO physical attempt fence is stale")
	ErrAttemptProof           = errors.New("RWO physical attempt proof is invalid")
	ErrAttemptRetryExhausted  = errors.New("RWO physical attempt send budget is exhausted")
	ErrAttemptSessionConflict = errors.New("RWO physical attempt session conflicts with durable mapping")
	ErrAttemptCorrupt         = errors.New("corrupt RWO physical attempt journal")
)

// AttemptState is physical coordination state only. It is never a semantic
// outcome and cannot allocate another RWO command.
type AttemptState string

type AttemptPreparation struct {
	CommandIntentIdentity string
	AdapterProfile        string
	AttemptOrdinal        uint64
	MaxSendTries          uint64
}

type AttemptFence struct {
	AttemptID string
	Owner     string
	Epoch     uint64
}

type RequestBinding struct {
	RequestFingerprint   string
	RequestPayloadSHA256 string
}

type SendTryLineage struct {
	AttemptID            string
	SendTryOrdinal       uint64
	SendTryID            string
	RequestFingerprint   string
	RequestPayloadSHA256 string
	FenceEpoch           uint64
}

type DeliveryAmbiguity struct {
	Code        string
	EvidenceRef string
}

// AttemptSnapshot is rebuilt solely from verified attempt-journal records.
type AttemptSnapshot struct {
	AttemptID             string
	CommandIntentIdentity string
	AdapterProfile        string
	AttemptOrdinal        uint64
	MaxSendTries          uint64
	State                 AttemptState
	SendTryOrdinal        uint64
	SendTryID             string
	RequestFingerprint    string
	RequestPayloadSHA256  string
	LeaseOwner            string
	LeaseDeadline         time.Time
	FenceEpoch            uint64
	ArmedFenceEpoch       uint64
	SessionID             string
	LastEventID           string
	ReasonCode            string
	EvidenceRef           string
}

type attemptJournalRecord struct {
	Transition            string `json:"transition"`
	AttemptID             string `json:"attempt_id"`
	CommandIntentIdentity string `json:"command_intent_identity,omitempty"`
	AdapterProfile        string `json:"adapter_profile,omitempty"`
	AttemptOrdinal        uint64 `json:"attempt_ordinal,omitempty"`
	MaxSendTries          uint64 `json:"max_send_tries,omitempty"`
	SendTryOrdinal        uint64 `json:"send_try_ordinal,omitempty"`
	SendTryID             string `json:"send_try_id,omitempty"`
	RequestFingerprint    string `json:"request_fingerprint,omitempty"`
	RequestPayloadSHA256  string `json:"request_payload_sha256,omitempty"`
	LeaseOwner            string `json:"lease_owner,omitempty"`
	LeaseDeadlineUnixNano int64  `json:"lease_deadline_unix_nano,omitempty"`
	FenceEpoch            uint64 `json:"fence_epoch,omitempty"`
	ArmedFenceEpoch       uint64 `json:"armed_fence_epoch,omitempty"`
	SessionID             string `json:"session_id,omitempty"`
	LastEventID           string `json:"last_event_id,omitempty"`
	ReasonCode            string `json:"reason_code,omitempty"`
	EvidenceRef           string `json:"evidence_ref,omitempty"`
}

func (attemptJournalRecord) DurableRecordType() DurableRecordType {
	return RecordTypeAttemptJournalV1
}

// AttemptCoordinator serializes one process's transition construction. The
// durable store sequence remains the authority between coordinator instances.
type AttemptCoordinator struct {
	store *DurableStore
	mu    sync.Mutex
}

type attemptProjectionState struct {
	attempts map[string]AttemptSnapshot
	snapshot DurableStoreSnapshot
}

func NewAttemptCoordinator(store *DurableStore) (*AttemptCoordinator, error) {
	if store == nil {
		return nil, fmt.Errorf("%w: durable store is required", ErrAttemptInvalid)
	}
	coordinator := &AttemptCoordinator{store: store}
	if _, err := coordinator.project(); err != nil {
		return nil, err
	}
	return coordinator, nil
}

func PhysicalAttemptID(commandIdentity, adapterProfile string, attemptOrdinal uint64) (string, error) {
	if commandIdentity == "" || adapterProfile == "" || attemptOrdinal == 0 {
		return "", fmt.Errorf("%w: command identity, adapter profile, and positive ordinal are required", ErrAttemptInvalid)
	}
	return identityDigest("RWO-PHYSICAL-ATTEMPT-V1\x00" + commandIdentity + adapterProfile + strconv.FormatUint(attemptOrdinal, 10)), nil
}

func PhysicalSendTryID(attemptID string, sendTryOrdinal uint64, requestFingerprint string) (string, error) {
	if attemptID == "" || sendTryOrdinal == 0 {
		return "", fmt.Errorf("%w: attempt identity and positive send-try ordinal are required", ErrAttemptInvalid)
	}
	if err := validateDigest(requestFingerprint); err != nil {
		return "", fmt.Errorf("%w: request fingerprint: %v", ErrAttemptInvalid, err)
	}
	return identityDigest("RWO-SEND-TRY-V1\x00" + attemptID + strconv.FormatUint(sendTryOrdinal, 10) + requestFingerprint), nil
}

func identityDigest(value string) string {
	digest := sha256.Sum256([]byte(value))
	return hex.EncodeToString(digest[:])
}

func (coordinator *AttemptCoordinator) Prepare(preparation AttemptPreparation) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	if preparation.AttemptOrdinal == 0 {
		preparation.AttemptOrdinal = 1
	}
	if preparation.MaxSendTries == 0 {
		return AttemptSnapshot{}, fmt.Errorf("%w: max send tries must be positive", ErrAttemptInvalid)
	}
	attemptID, err := PhysicalAttemptID(preparation.CommandIntentIdentity, preparation.AdapterProfile, preparation.AttemptOrdinal)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	projection, err := coordinator.projectWithSnapshot()
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if err := requireDurableOutboxCommand(projection.snapshot, preparation.CommandIntentIdentity); err != nil {
		return AttemptSnapshot{}, err
	}
	if current, exists := projection.attempts[attemptID]; exists {
		if current.CommandIntentIdentity == preparation.CommandIntentIdentity && current.AdapterProfile == preparation.AdapterProfile && current.AttemptOrdinal == preparation.AttemptOrdinal && current.MaxSendTries == preparation.MaxSendTries {
			return current, nil
		}
		return AttemptSnapshot{}, ErrAttemptConflict
	}
	record := attemptJournalRecord{
		Transition: attemptTransitionPrepared, AttemptID: attemptID,
		CommandIntentIdentity: preparation.CommandIntentIdentity, AdapterProfile: preparation.AdapterProfile,
		AttemptOrdinal: preparation.AttemptOrdinal, MaxSendTries: preparation.MaxSendTries, SendTryOrdinal: 1,
	}
	if err := coordinator.append(record, projection.snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(attemptID)
}

func (coordinator *AttemptCoordinator) Claim(attemptID, owner string, now time.Time, ttl time.Duration) (AttemptFence, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	if owner == "" || now.IsZero() || ttl <= 0 {
		return AttemptFence{}, fmt.Errorf("%w: owner, current time, and positive TTL are required", ErrAttemptInvalid)
	}
	current, snapshot, err := coordinator.currentWithSnapshot(attemptID)
	if err != nil {
		return AttemptFence{}, err
	}
	if terminalAttemptState(current.State) {
		return AttemptFence{}, ErrAttemptTransition
	}
	if current.LeaseOwner == owner && current.FenceEpoch != 0 && now.Before(current.LeaseDeadline) {
		return AttemptFence{AttemptID: attemptID, Owner: owner, Epoch: current.FenceEpoch}, nil
	}
	if current.LeaseOwner != "" && current.LeaseOwner != owner && now.Before(current.LeaseDeadline) {
		return AttemptFence{}, ErrAttemptLeaseHeld
	}
	record := coordinator.recordFrom(current, attemptTransitionLeaseClaimed)
	record.LeaseOwner = owner
	record.LeaseDeadlineUnixNano = now.Add(ttl).UTC().UnixNano()
	record.FenceEpoch = current.FenceEpoch + 1
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptFence{}, err
	}
	return AttemptFence{AttemptID: attemptID, Owner: owner, Epoch: record.FenceEpoch}, nil
}

func (coordinator *AttemptCoordinator) ArmSend(fence AttemptFence, binding RequestBinding) (SendTryLineage, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return SendTryLineage{}, err
	}
	if current.State != AttemptPrepared {
		return SendTryLineage{}, ErrAttemptTransition
	}
	if err := validateDigest(binding.RequestFingerprint); err != nil {
		return SendTryLineage{}, fmt.Errorf("%w: request fingerprint: %v", ErrAttemptInvalid, err)
	}
	if err := validateDigest(binding.RequestPayloadSHA256); err != nil {
		return SendTryLineage{}, fmt.Errorf("%w: request payload digest: %v", ErrAttemptInvalid, err)
	}
	if current.RequestPayloadSHA256 != "" && current.RequestPayloadSHA256 != binding.RequestPayloadSHA256 {
		return SendTryLineage{}, ErrAttemptConflict
	}
	sendTryID, err := PhysicalSendTryID(current.AttemptID, current.SendTryOrdinal, binding.RequestFingerprint)
	if err != nil {
		return SendTryLineage{}, err
	}
	record := coordinator.recordFrom(current, attemptTransitionSendArmed)
	record.SendTryID = sendTryID
	record.RequestFingerprint = binding.RequestFingerprint
	record.RequestPayloadSHA256 = binding.RequestPayloadSHA256
	record.ArmedFenceEpoch = current.FenceEpoch
	if err := coordinator.append(record, snapshot); err != nil {
		return SendTryLineage{}, err
	}
	return lineageFromRecord(record), nil
}

type notSentProofKind string

const (
	notSentLive           notSentProofKind = "live_zero_bytes"
	notSentReconciliation notSentProofKind = "bound_reconciliation"
)

type KnownNotSentProof struct {
	kind               notSentProofKind
	lineage            SendTryLineage
	reasonCode         string
	evidenceRef        string
	reconciliationAuth string
}

func NewLiveKnownNotSentProof(lineage SendTryLineage, typedErrorCode, observationRef string) (KnownNotSentProof, error) {
	if err := validateLineage(lineage); err != nil || typedErrorCode == "" || observationRef == "" {
		return KnownNotSentProof{}, fmt.Errorf("%w: exact live zero-byte observation is required", ErrAttemptProof)
	}
	return KnownNotSentProof{kind: notSentLive, lineage: lineage, reasonCode: typedErrorCode, evidenceRef: observationRef}, nil
}

func NewBoundNotSentReconciliation(lineage SendTryLineage, proofRef, continuationAuthorityRef string) (KnownNotSentProof, error) {
	if err := validateLineage(lineage); err != nil || proofRef == "" || continuationAuthorityRef == "" {
		return KnownNotSentProof{}, fmt.Errorf("%w: bound proof and continuation authority are required", ErrAttemptProof)
	}
	return KnownNotSentProof{kind: notSentReconciliation, lineage: lineage, reasonCode: "RECONCILED_NOT_SENT", evidenceRef: proofRef, reconciliationAuth: continuationAuthorityRef}, nil
}

func (coordinator *AttemptCoordinator) MarkKnownNotSent(fence AttemptFence, proof KnownNotSentProof) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if err := exactLineage(current, proof.lineage); err != nil {
		return AttemptSnapshot{}, err
	}
	if proof.kind == notSentLive && current.State != AttemptSendArmed {
		return AttemptSnapshot{}, ErrAttemptProof
	}
	if proof.kind == notSentReconciliation && (current.State != AttemptDeliveryUnknown || proof.reconciliationAuth == "") {
		return AttemptSnapshot{}, ErrAttemptProof
	}
	if proof.kind != notSentLive && proof.kind != notSentReconciliation {
		return AttemptSnapshot{}, ErrAttemptProof
	}
	record := coordinator.recordFrom(current, attemptTransitionKnownNotSent)
	record.ReasonCode, record.EvidenceRef = proof.reasonCode, proof.evidenceRef
	if proof.kind == notSentReconciliation {
		record.EvidenceRef += "|authority=" + proof.reconciliationAuth
	}
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

func (coordinator *AttemptCoordinator) AllocateNextSendTry(fence AttemptFence) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if current.State != AttemptKnownNotSent {
		return AttemptSnapshot{}, ErrAttemptTransition
	}
	if current.SendTryOrdinal >= current.MaxSendTries {
		record := coordinator.recordFrom(current, attemptTransitionBlocked)
		record.ReasonCode = "RETRY_EXHAUSTED"
		if appendErr := coordinator.append(record, snapshot); appendErr != nil {
			return AttemptSnapshot{}, appendErr
		}
		return AttemptSnapshot{}, ErrAttemptRetryExhausted
	}
	record := coordinator.recordFrom(current, attemptTransitionSendTryAllocated)
	record.SendTryOrdinal++
	record.SendTryID, record.RequestFingerprint = "", ""
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

func (coordinator *AttemptCoordinator) MarkDeliveryUnknown(fence AttemptFence, lineage SendTryLineage, observation DeliveryAmbiguity) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	if observation.Code == "" || observation.EvidenceRef == "" {
		return AttemptSnapshot{}, fmt.Errorf("%w: ambiguity code and evidence are required", ErrAttemptInvalid)
	}
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if current.State != AttemptSendArmed {
		return AttemptSnapshot{}, ErrAttemptTransition
	}
	if err := exactLineage(current, lineage); err != nil {
		return AttemptSnapshot{}, err
	}
	record := coordinator.recordFrom(current, attemptTransitionDeliveryUnknown)
	record.ReasonCode, record.EvidenceRef = observation.Code, observation.EvidenceRef
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

// RecoverAfterReopen freezes every persisted armed send as delivery_unknown.
// It performs no adapter call and is deliberately explicit: constructing a
// coordinator immediately before the one live create must not trigger it.
func (coordinator *AttemptCoordinator) RecoverAfterReopen() (int, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	projection, err := coordinator.project()
	if err != nil {
		return 0, err
	}
	armedIDs := make([]string, 0)
	for attemptID, current := range projection {
		if current.State == AttemptSendArmed {
			armedIDs = append(armedIDs, attemptID)
		}
	}
	sort.Strings(armedIDs)
	recovered := 0
	for _, attemptID := range armedIDs {
		current, snapshot, currentErr := coordinator.currentWithSnapshot(attemptID)
		if currentErr != nil {
			return recovered, currentErr
		}
		if current.State != AttemptSendArmed {
			continue
		}
		record := coordinator.recordFrom(current, attemptTransitionDeliveryUnknown)
		record.ReasonCode, record.EvidenceRef = "RECOVERED_FROM_SEND_ARMED", "verified-reopen"
		if err := coordinator.append(record, snapshot); err != nil {
			return recovered, err
		}
		recovered++
	}
	return recovered, nil
}

func (coordinator *AttemptCoordinator) MapSession(fence AttemptFence, lineage SendTryLineage, sessionID, responseSHA256 string) (AttemptSnapshot, error) {
	return coordinator.mapSession(fence, lineage, sessionID, responseSHA256, false)
}

type LateSessionProof struct {
	lineage        SendTryLineage
	sessionID      string
	responseSHA256 string
	evidenceRef    string
}

func NewCorrelatedLateSessionProof(lineage SendTryLineage, sessionID, responseSHA256, evidenceRef string) (LateSessionProof, error) {
	if err := validateLineage(lineage); err != nil || sessionID == "" || evidenceRef == "" {
		return LateSessionProof{}, fmt.Errorf("%w: exact late response lineage is required", ErrAttemptProof)
	}
	if err := validateDigest(responseSHA256); err != nil {
		return LateSessionProof{}, fmt.Errorf("%w: response digest: %v", ErrAttemptProof, err)
	}
	return LateSessionProof{lineage: lineage, sessionID: sessionID, responseSHA256: responseSHA256, evidenceRef: evidenceRef}, nil
}

func (coordinator *AttemptCoordinator) CorrelateLateSession(fence AttemptFence, proof LateSessionProof) (AttemptSnapshot, error) {
	if proof.evidenceRef == "" {
		return AttemptSnapshot{}, ErrAttemptProof
	}
	return coordinator.mapSession(fence, proof.lineage, proof.sessionID, proof.responseSHA256, true)
}

func (coordinator *AttemptCoordinator) mapSession(fence AttemptFence, lineage SendTryLineage, sessionID, responseSHA256 string, late bool) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	if sessionID == "" {
		return AttemptSnapshot{}, fmt.Errorf("%w: session ID is required", ErrAttemptInvalid)
	}
	if err := validateDigest(responseSHA256); err != nil {
		return AttemptSnapshot{}, fmt.Errorf("%w: response digest: %v", ErrAttemptInvalid, err)
	}
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if current.SessionID != "" {
		if current.SessionID == sessionID && exactLineage(current, lineage) == nil {
			return current, nil
		}
		record := coordinator.recordFrom(current, attemptTransitionUncorrelatedSession)
		record.SessionID, record.ReasonCode, record.EvidenceRef = sessionID, "CONFLICTING_SESSION", responseSHA256
		if appendErr := coordinator.append(record, snapshot); appendErr != nil {
			return AttemptSnapshot{}, appendErr
		}
		return AttemptSnapshot{}, ErrAttemptSessionConflict
	}
	if (!late && current.State != AttemptSendArmed) || (late && current.State != AttemptDeliveryUnknown) {
		return AttemptSnapshot{}, ErrAttemptTransition
	}
	if err := exactLineage(current, lineage); err != nil {
		return AttemptSnapshot{}, err
	}
	record := coordinator.recordFrom(current, attemptTransitionSessionKnown)
	record.SessionID, record.EvidenceRef = sessionID, responseSHA256
	if late {
		record.ReasonCode = "LATE_CORRELATED"
	}
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

func (coordinator *AttemptCoordinator) AttachStream(fence AttemptFence, sessionID, lastEventID string) (AttemptSnapshot, error) {
	return coordinator.simpleSessionTransition(fence, sessionID, attemptTransitionStreamAttached, AttemptSessionKnown, lastEventID, "")
}

func (coordinator *AttemptCoordinator) DetachStream(fence AttemptFence, sessionID, evidenceRef string) (AttemptSnapshot, error) {
	return coordinator.simpleSessionTransition(fence, sessionID, attemptTransitionStreamDetached, AttemptStreamAttached, "", evidenceRef)
}

func (coordinator *AttemptCoordinator) RequestCancel(fence AttemptFence, sessionID, authorizationRef string) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	if authorizationRef == "" {
		return AttemptSnapshot{}, fmt.Errorf("%w: cancel authorization is required", ErrAttemptProof)
	}
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if current.SessionID != sessionID || (current.State != AttemptSessionKnown && current.State != AttemptStreamAttached) {
		return AttemptSnapshot{}, ErrAttemptTransition
	}
	record := coordinator.recordFrom(current, attemptTransitionCancelRequested)
	record.EvidenceRef = authorizationRef
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

func (coordinator *AttemptCoordinator) Block(fence AttemptFence, code, evidenceRef string) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	if code == "" || evidenceRef == "" {
		return AttemptSnapshot{}, fmt.Errorf("%w: block code and evidence are required", ErrAttemptInvalid)
	}
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if terminalAttemptState(current.State) {
		return AttemptSnapshot{}, ErrAttemptTransition
	}
	record := coordinator.recordFrom(current, attemptTransitionBlocked)
	record.ReasonCode, record.EvidenceRef = code, evidenceRef
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

type TerminalAdmissionProof struct {
	attemptID              string
	sessionID              string
	admissionKey           string
	semanticCommitSequence uint64
}

func NewTerminalAdmissionProof(attemptID, sessionID, admissionKey string, semanticCommitSequence uint64) (TerminalAdmissionProof, error) {
	if attemptID == "" || sessionID == "" || !isTaggedSHA256(admissionKey) || semanticCommitSequence == 0 {
		return TerminalAdmissionProof{}, fmt.Errorf("%w: synced terminal admission binding is required", ErrAttemptProof)
	}
	return TerminalAdmissionProof{attemptID: attemptID, sessionID: sessionID, admissionKey: admissionKey, semanticCommitSequence: semanticCommitSequence}, nil
}

func (coordinator *AttemptCoordinator) Acknowledge(fence AttemptFence, proof TerminalAdmissionProof) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if proof.attemptID != current.AttemptID || proof.sessionID == "" || proof.sessionID != current.SessionID ||
		!isTaggedSHA256(proof.admissionKey) || proof.semanticCommitSequence == 0 {
		return AttemptSnapshot{}, ErrAttemptProof
	}
	if err := requireExactTerminalAdmission(snapshot, proof); err != nil {
		return AttemptSnapshot{}, err
	}
	if current.State != AttemptSessionKnown && current.State != AttemptStreamAttached && current.State != AttemptCancelRequested {
		return AttemptSnapshot{}, ErrAttemptTransition
	}
	record := coordinator.recordFrom(current, attemptTransitionAcknowledged)
	record.EvidenceRef = proof.admissionKey + "|semantic_sequence=" + strconv.FormatUint(proof.semanticCommitSequence, 10)
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

func (coordinator *AttemptCoordinator) Snapshot(attemptID string) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	return coordinator.current(attemptID)
}

func (coordinator *AttemptCoordinator) simpleSessionTransition(fence AttemptFence, sessionID, transition string, required AttemptState, lastEventID, evidenceRef string) (AttemptSnapshot, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	current, snapshot, err := coordinator.currentFenced(fence)
	if err != nil {
		return AttemptSnapshot{}, err
	}
	if current.State != required || current.SessionID == "" || current.SessionID != sessionID {
		return AttemptSnapshot{}, ErrAttemptTransition
	}
	record := coordinator.recordFrom(current, transition)
	record.LastEventID, record.EvidenceRef = lastEventID, evidenceRef
	if err := coordinator.append(record, snapshot); err != nil {
		return AttemptSnapshot{}, err
	}
	return coordinator.snapshotAfter(current.AttemptID)
}

func (coordinator *AttemptCoordinator) currentFenced(fence AttemptFence) (AttemptSnapshot, DurableStoreSnapshot, error) {
	current, snapshot, err := coordinator.currentWithSnapshot(fence.AttemptID)
	if err != nil {
		return AttemptSnapshot{}, DurableStoreSnapshot{}, err
	}
	if fence.Owner == "" || current.FenceEpoch == 0 || current.FenceEpoch != fence.Epoch || current.LeaseOwner != fence.Owner {
		return AttemptSnapshot{}, DurableStoreSnapshot{}, ErrAttemptStaleFence
	}
	return current, snapshot, nil
}

func (coordinator *AttemptCoordinator) current(attemptID string) (AttemptSnapshot, error) {
	if attemptID == "" {
		return AttemptSnapshot{}, ErrAttemptNotFound
	}
	projection, err := coordinator.project()
	if err != nil {
		return AttemptSnapshot{}, err
	}
	current, exists := projection[attemptID]
	if !exists {
		return AttemptSnapshot{}, ErrAttemptNotFound
	}
	return current, nil
}

func (coordinator *AttemptCoordinator) currentWithSnapshot(attemptID string) (AttemptSnapshot, DurableStoreSnapshot, error) {
	if attemptID == "" {
		return AttemptSnapshot{}, DurableStoreSnapshot{}, ErrAttemptNotFound
	}
	projection, err := coordinator.projectWithSnapshot()
	if err != nil {
		return AttemptSnapshot{}, DurableStoreSnapshot{}, err
	}
	current, exists := projection.attempts[attemptID]
	if !exists {
		return AttemptSnapshot{}, DurableStoreSnapshot{}, ErrAttemptNotFound
	}
	return current, projection.snapshot, nil
}

func (coordinator *AttemptCoordinator) snapshotAfter(attemptID string) (AttemptSnapshot, error) {
	return coordinator.current(attemptID)
}

func (coordinator *AttemptCoordinator) append(record attemptJournalRecord, snapshot DurableStoreSnapshot) error {
	_, err := coordinator.store.Append(AppendExpectation{
		ExpectedSequence: snapshot.LastSequence + 1, ExpectedPreviousFrameSHA256: snapshot.LastFrameSHA256,
	}, record)
	return err
}

func (coordinator *AttemptCoordinator) project() (map[string]AttemptSnapshot, error) {
	projection, err := coordinator.projectWithSnapshot()
	if err != nil {
		return nil, err
	}
	return projection.attempts, nil
}

func (coordinator *AttemptCoordinator) projectWithSnapshot() (attemptProjectionState, error) {
	snapshot, err := coordinator.store.Snapshot()
	if err != nil {
		return attemptProjectionState{}, err
	}
	projection := make(map[string]AttemptSnapshot)
	for _, stored := range snapshot.Records {
		if stored.Type != RecordTypeAttemptJournalV1 {
			continue
		}
		var record attemptJournalRecord
		if err := decodeClosedJSON(stored.Body, &record); err != nil {
			return attemptProjectionState{}, fmt.Errorf("%w at sequence %d: %v", ErrAttemptCorrupt, stored.Ref.Sequence, err)
		}
		if err := applyAttemptRecord(projection, record); err != nil {
			return attemptProjectionState{}, fmt.Errorf("%w at sequence %d: %v", ErrAttemptCorrupt, stored.Ref.Sequence, err)
		}
	}
	for _, current := range projection {
		if err := requireDurableOutboxCommand(snapshot, current.CommandIntentIdentity); err != nil {
			return attemptProjectionState{}, fmt.Errorf("%w: attempt %s has no verified outbox command: %v", ErrAttemptCorrupt, current.AttemptID, err)
		}
	}
	return attemptProjectionState{attempts: projection, snapshot: snapshot}, nil
}

// requireDurableOutboxCommand prevents the physical machine from inventing a
// semantic command identity. The command must be present in a verified
// SemanticCommitV1 frame in the same store before attempt_prepared can append.
func requireDurableOutboxCommand(snapshot DurableStoreSnapshot, commandIdentity string) error {
	if !isTaggedSHA256(commandIdentity) {
		return fmt.Errorf("%w: Rust command identity is required", ErrAttemptInvalid)
	}
	var committed []byte
	for _, stored := range snapshot.Records {
		if stored.Type != RecordTypeSemanticCommitV1 {
			continue
		}
		var record SemanticCommitV1
		if err := decodeClosedJSON(stored.Body, &record); err != nil {
			return fmt.Errorf("%w: semantic commit %d", ErrAttemptCorrupt, stored.Ref.Sequence)
		}
		response, _, err := validateStoredSemanticCommit(record, snapshot.Header.GraphIdentity, stored.Cursor)
		if err != nil {
			return fmt.Errorf("%w: semantic commit %d: %v", ErrAttemptCorrupt, stored.Ref.Sequence, err)
		}
		if response.CommandIntentIdentity != commandIdentity {
			continue
		}
		if len(response.CommandIntent) == 0 {
			return fmt.Errorf("%w: command identity has no committed bytes", ErrAttemptCorrupt)
		}
		if committed != nil && !bytes.Equal(committed, response.CommandIntent) {
			return fmt.Errorf("%w: command identity binds conflicting bytes", ErrAttemptCorrupt)
		}
		committed = cloneBytes(response.CommandIntent)
	}
	if committed == nil {
		return fmt.Errorf("%w: command is absent from the durable Rust outbox", ErrAttemptProof)
	}
	return nil
}

// requireExactTerminalAdmission binds physical acknowledgement to the synced
// Rust no-successor commit and the terminal-admission marker that names this
// exact attempt and session. Opaque caller prose cannot manufacture success.
func requireExactTerminalAdmission(snapshot DurableStoreSnapshot, proof TerminalAdmissionProof) error {
	var semanticIdentity string
	for _, stored := range snapshot.Records {
		if stored.Ref.Sequence != proof.semanticCommitSequence {
			continue
		}
		if stored.Type != RecordTypeSemanticCommitV1 {
			return ErrAttemptProof
		}
		var semantic SemanticCommitV1
		if err := decodeClosedJSON(stored.Body, &semantic); err != nil {
			return ErrAttemptCorrupt
		}
		response, _, err := validateStoredSemanticCommit(semantic, snapshot.Header.GraphIdentity, stored.Cursor)
		if err != nil || response.Outcome != "Applied" || len(response.CommandIntent) != 0 {
			return ErrAttemptProof
		}
		semanticIdentity = response.AcceptedEventIdentity
		break
	}
	if semanticIdentity == "" {
		return ErrAttemptProof
	}
	for _, stored := range snapshot.Records {
		if stored.Type != RecordTypeTerminalAdmissionV1 {
			continue
		}
		var admission terminalAdmissionRecord
		if err := decodeClosedJSON(stored.Body, &admission); err != nil {
			return ErrAttemptCorrupt
		}
		if admission.AdmissionKey == proof.admissionKey && admission.AttemptID == proof.attemptID &&
			admission.SessionID == proof.sessionID && admission.SemanticCommitSequence == proof.semanticCommitSequence &&
			admission.AcceptedEventIdentity == semanticIdentity && stored.Ref.Sequence > proof.semanticCommitSequence {
			return nil
		}
	}
	return ErrAttemptProof
}

func applyAttemptRecord(projection map[string]AttemptSnapshot, record attemptJournalRecord) error {
	if record.AttemptID == "" || record.Transition == "" {
		return ErrAttemptInvalid
	}
	current, exists := projection[record.AttemptID]
	if record.Transition == attemptTransitionPrepared {
		if exists || !isTaggedSHA256(record.CommandIntentIdentity) || record.AdapterProfile == "" || record.AttemptOrdinal == 0 || record.MaxSendTries == 0 || record.SendTryOrdinal != 1 {
			return ErrAttemptConflict
		}
		projection[record.AttemptID] = AttemptSnapshot{
			AttemptID: record.AttemptID, CommandIntentIdentity: record.CommandIntentIdentity, AdapterProfile: record.AdapterProfile,
			AttemptOrdinal: record.AttemptOrdinal, MaxSendTries: record.MaxSendTries, State: AttemptPrepared, SendTryOrdinal: 1,
		}
		return nil
	}
	if !exists || record.CommandIntentIdentity != current.CommandIntentIdentity || record.AdapterProfile != current.AdapterProfile || record.AttemptOrdinal != current.AttemptOrdinal || record.MaxSendTries != current.MaxSendTries {
		return ErrAttemptConflict
	}
	if record.Transition != attemptTransitionLeaseClaimed && (record.FenceEpoch != current.FenceEpoch || record.LeaseOwner != current.LeaseOwner) {
		return ErrAttemptStaleFence
	}
	next := current
	switch record.Transition {
	case attemptTransitionLeaseClaimed:
		if terminalAttemptState(current.State) || record.FenceEpoch != current.FenceEpoch+1 || record.LeaseOwner == "" || record.LeaseDeadlineUnixNano == 0 {
			return ErrAttemptTransition
		}
		next.LeaseOwner, next.FenceEpoch = record.LeaseOwner, record.FenceEpoch
		next.LeaseDeadline = time.Unix(0, record.LeaseDeadlineUnixNano).UTC()
	case attemptTransitionSendArmed:
		if current.State != AttemptPrepared || record.SendTryOrdinal != current.SendTryOrdinal || record.SendTryID == "" || record.RequestFingerprint == "" || record.RequestPayloadSHA256 == "" || record.ArmedFenceEpoch != current.FenceEpoch {
			return ErrAttemptTransition
		}
		next.State, next.SendTryID, next.RequestFingerprint, next.RequestPayloadSHA256, next.ArmedFenceEpoch = AttemptSendArmed, record.SendTryID, record.RequestFingerprint, record.RequestPayloadSHA256, record.ArmedFenceEpoch
	case attemptTransitionKnownNotSent:
		if (current.State != AttemptSendArmed && current.State != AttemptDeliveryUnknown) || record.SendTryID != current.SendTryID || record.RequestFingerprint != current.RequestFingerprint || record.ReasonCode == "" || record.EvidenceRef == "" {
			return ErrAttemptTransition
		}
		next.State, next.ReasonCode, next.EvidenceRef = AttemptKnownNotSent, record.ReasonCode, record.EvidenceRef
	case attemptTransitionSendTryAllocated:
		if current.State != AttemptKnownNotSent || record.SendTryOrdinal != current.SendTryOrdinal+1 || record.SendTryOrdinal > current.MaxSendTries || record.SendTryID != "" || record.RequestFingerprint != "" {
			return ErrAttemptTransition
		}
		next.State, next.SendTryOrdinal, next.SendTryID, next.RequestFingerprint, next.ArmedFenceEpoch = AttemptPrepared, record.SendTryOrdinal, "", "", 0
		next.ReasonCode, next.EvidenceRef = "", ""
	case attemptTransitionDeliveryUnknown:
		if current.State != AttemptSendArmed || record.SendTryID != current.SendTryID || record.RequestFingerprint != current.RequestFingerprint || record.ReasonCode == "" {
			return ErrAttemptTransition
		}
		next.State, next.ReasonCode, next.EvidenceRef = AttemptDeliveryUnknown, record.ReasonCode, record.EvidenceRef
	case attemptTransitionSessionKnown:
		if (current.State != AttemptSendArmed && current.State != AttemptDeliveryUnknown) || current.SessionID != "" || record.SessionID == "" || record.SendTryID != current.SendTryID || record.RequestFingerprint != current.RequestFingerprint {
			return ErrAttemptTransition
		}
		next.State, next.SessionID, next.ReasonCode, next.EvidenceRef = AttemptSessionKnown, record.SessionID, record.ReasonCode, record.EvidenceRef
	case attemptTransitionStreamAttached:
		if current.State != AttemptSessionKnown || record.SessionID != current.SessionID {
			return ErrAttemptTransition
		}
		next.State, next.LastEventID = AttemptStreamAttached, record.LastEventID
	case attemptTransitionStreamDetached:
		if current.State != AttemptStreamAttached || record.SessionID != current.SessionID {
			return ErrAttemptTransition
		}
		next.State, next.EvidenceRef = AttemptSessionKnown, record.EvidenceRef
	case attemptTransitionCancelRequested:
		if (current.State != AttemptSessionKnown && current.State != AttemptStreamAttached) || record.SessionID != current.SessionID || record.EvidenceRef == "" {
			return ErrAttemptTransition
		}
		next.State, next.EvidenceRef = AttemptCancelRequested, record.EvidenceRef
	case attemptTransitionBlocked, attemptTransitionUncorrelatedSession:
		if terminalAttemptState(current.State) || record.ReasonCode == "" {
			return ErrAttemptTransition
		}
		next.State, next.ReasonCode, next.EvidenceRef = AttemptBlocked, record.ReasonCode, record.EvidenceRef
	case attemptTransitionAcknowledged:
		if (current.State != AttemptSessionKnown && current.State != AttemptStreamAttached && current.State != AttemptCancelRequested) || record.SessionID != current.SessionID || record.EvidenceRef == "" {
			return ErrAttemptTransition
		}
		next.State, next.EvidenceRef = AttemptAcknowledged, record.EvidenceRef
	default:
		return ErrAttemptTransition
	}
	projection[record.AttemptID] = next
	return nil
}

func (coordinator *AttemptCoordinator) recordFrom(current AttemptSnapshot, transition string) attemptJournalRecord {
	return attemptJournalRecord{
		Transition: transition, AttemptID: current.AttemptID, CommandIntentIdentity: current.CommandIntentIdentity,
		AdapterProfile: current.AdapterProfile, AttemptOrdinal: current.AttemptOrdinal, MaxSendTries: current.MaxSendTries,
		SendTryOrdinal: current.SendTryOrdinal, SendTryID: current.SendTryID, RequestFingerprint: current.RequestFingerprint,
		RequestPayloadSHA256: current.RequestPayloadSHA256, LeaseOwner: current.LeaseOwner,
		LeaseDeadlineUnixNano: current.LeaseDeadline.UnixNano(), FenceEpoch: current.FenceEpoch, SessionID: current.SessionID,
		ArmedFenceEpoch: current.ArmedFenceEpoch, LastEventID: current.LastEventID, ReasonCode: current.ReasonCode, EvidenceRef: current.EvidenceRef,
	}
}

func lineageFromRecord(record attemptJournalRecord) SendTryLineage {
	return SendTryLineage{AttemptID: record.AttemptID, SendTryOrdinal: record.SendTryOrdinal, SendTryID: record.SendTryID, RequestFingerprint: record.RequestFingerprint, RequestPayloadSHA256: record.RequestPayloadSHA256, FenceEpoch: record.FenceEpoch}
}

func validateLineage(lineage SendTryLineage) error {
	if lineage.AttemptID == "" || lineage.SendTryOrdinal == 0 || lineage.SendTryID == "" || lineage.FenceEpoch == 0 {
		return ErrAttemptProof
	}
	if err := validateDigest(lineage.RequestFingerprint); err != nil {
		return ErrAttemptProof
	}
	if err := validateDigest(lineage.RequestPayloadSHA256); err != nil {
		return ErrAttemptProof
	}
	return nil
}

func exactLineage(current AttemptSnapshot, lineage SendTryLineage) error {
	if validateLineage(lineage) != nil || current.AttemptID != lineage.AttemptID || current.SendTryOrdinal != lineage.SendTryOrdinal || current.SendTryID != lineage.SendTryID || current.RequestFingerprint != lineage.RequestFingerprint || current.RequestPayloadSHA256 != lineage.RequestPayloadSHA256 || current.ArmedFenceEpoch != lineage.FenceEpoch {
		return ErrAttemptProof
	}
	return nil
}

func terminalAttemptState(state AttemptState) bool {
	return state == AttemptBlocked || state == AttemptAcknowledged
}
