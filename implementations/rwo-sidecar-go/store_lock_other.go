//go:build !linux

package rwosidecar

import "os"

func lockStoreFile(_ *os.File) error {
	return ErrDurableStoreLockUnsupported
}

func unlockStoreFile(_ *os.File) error {
	return nil
}
