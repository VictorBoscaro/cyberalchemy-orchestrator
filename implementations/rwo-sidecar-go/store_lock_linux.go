//go:build linux

package rwosidecar

import (
	"errors"
	"fmt"
	"os"

	"golang.org/x/sys/unix"
)

func lockStoreFile(file *os.File) error {
	if file == nil {
		return fmt.Errorf("%w: file is required", ErrDurableStoreLocked)
	}
	if err := unix.Flock(int(file.Fd()), unix.LOCK_EX|unix.LOCK_NB); err != nil {
		if errors.Is(err, unix.EWOULDBLOCK) || errors.Is(err, unix.EAGAIN) {
			return ErrDurableStoreLocked
		}
		return fmt.Errorf("%w: %v", ErrDurableStoreLocked, err)
	}
	return nil
}

func unlockStoreFile(file *os.File) error {
	if file == nil {
		return nil
	}
	if err := unix.Flock(int(file.Fd()), unix.LOCK_UN); err != nil {
		return fmt.Errorf("unlock RWO durable store: %w", err)
	}
	return nil
}
