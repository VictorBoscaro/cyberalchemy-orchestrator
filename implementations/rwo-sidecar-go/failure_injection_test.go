package rwosidecar

import (
	"os"
	"testing"
)

// TestDurableFailureMatrix executes the actual behavioral witnesses rather
// than checking a list of names. The real-child rows are mandatory here: a
// final campaign run without RWO_KERNEL_CHILD would be vacuous.
func TestDurableFailureMatrix(t *testing.T) {
	if os.Getenv("RWO_KERNEL_CHILD") == "" {
		t.Skip("set RWO_KERNEL_CHILD for the non-vacuous failure matrix")
	}
	type matrixRow struct {
		id      string
		witness func(*testing.T)
	}
	rows := []matrixRow{
		{"FM-01", TestDurableRuntimeCrashBeforeSemanticAppendLeavesNoState},
		{"FM-02", TestDurableStoreTornSemanticTailTruncatesToVerifiedPrefix},
		{"FM-03", TestSyncedSemanticCommitBeforeAckReplaysOneRustOutcome},
		{"FM-04", TestPreparedAttemptReopensAndSendsOnce},
		{"FM-05", TestCrashAfterSendArmedFreezesCreate},
		{"FM-06", func(t *testing.T) {
			t.Run("attempt", TestSessionKnownReopensByReconnect)
			t.Run("adapter", TestSessionKnownReopensByReconnectWithoutSecondCreate)
		}},
		{"FM-07", TestRawTerminalReopensAndAdmitsOnce},
		{"FM-08", TestTerminalCommitBeforeAckIsInertOnReopen},
		{"FM-09", TestDurableStoreInteriorCorruptionBlocksOpen},
		{"FM-10", func(t *testing.T) {
			t.Run("store-cas", TestDurableStoreStaleSequenceHashAndCursorRejectWithoutAppend)
			t.Run("attempt-fence", TestStaleFenceRejectsWithoutAppend)
		}},
		{"FM-11", TestFabricatedOrChangedCommandCannotCommit},
		{"FM-12", TestSingleSchedulerAblationRejectsSecondOwner},
		{"FM-13", TestKnownNotSentRetriesSameAttemptWithNextTry},
		{"FM-14", TestAmbiguousSendCannotRetryWithoutProof},
		{"FM-15", TestBoundNotSentReconciliationAllowsNextTry},
		{"FM-16", TestRequestPolicyMustBeExactAndToolFree},
		{"FM-17", TestForbiddenEveEventsCannotAdmit},
		{"FM-18", TestRepresentationVariantConvergesOnAdmissionKey},
		{"FM-19", TestSameAdmissionKeyDifferentDigestBlocks},
		{"FM-20", TestGovernanceFactsAreNotSeatOutput},
		{"FM-21", TestMaterialAddressRejectsAnyDrift},
		{"FM-22", TestDurableRuntimeNonAppliedAndMissingRustAreInert},
		{"FM-23", TestDurableStoreWriteOrSyncFailurePoisonsUntilVerifiedReopen},
		{"FM-24", TestCorrelatedLateResponseMapsWithoutRecreate},
		{"FM-25", TestContentAddressRoundTripsThroughRealRust},
		{"FM-26", TestContentAddressRoundTripRejectsDriftWrongSeatAndSubstitution},
		{"PC-01", TestOneSeatCompletesAcrossRustAndFakeEve},
		{"PC-02", TestEveryBoundaryReopenMatchesReference},
		{"PC-03", TestCommittedReplayPreservesRustOutcomeWithoutSecondOutbox},
		{"PC-04", TestIndependentStreamsShareStoreWithoutCrossTalk},
	}
	if len(rows) != 30 {
		t.Fatalf("failure-matrix rows = %d, want 30", len(rows))
	}
	seen := make(map[string]bool, len(rows))
	for _, row := range rows {
		if seen[row.id] || row.witness == nil {
			t.Fatalf("invalid matrix row %q", row.id)
		}
		seen[row.id] = true
		t.Run(row.id, row.witness)
	}
}
