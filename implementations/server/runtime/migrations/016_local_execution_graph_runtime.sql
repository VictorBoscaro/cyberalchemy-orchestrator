CREATE TABLE local_execution_admissions(
  admission_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL,
  revision TEXT NOT NULL,
  graph_digest TEXT NOT NULL,
  graph_bytes BLOB NOT NULL,
  authority_json TEXT NOT NULL,
  authority_digest TEXT NOT NULL,
  dispatch_sequence INTEGER NOT NULL CHECK(dispatch_sequence>=1),
  UNIQUE(dispatch_id,revision),
  UNIQUE(dispatch_id,dispatch_sequence)
);

CREATE TABLE local_execution_runs(
  run_id TEXT PRIMARY KEY,
  admission_id TEXT NOT NULL UNIQUE REFERENCES local_execution_admissions(admission_id),
  status TEXT NOT NULL CHECK(status IN ('pending','running','succeeded','failed','cancelled','stopped')),
  cancel_requested INTEGER NOT NULL DEFAULT 0 CHECK(cancel_requested IN (0,1)),
  next_receipt_sequence INTEGER NOT NULL DEFAULT 0 CHECK(next_receipt_sequence>=0),
  terminal_reason TEXT
);

CREATE TABLE local_execution_nodes(
  run_id TEXT NOT NULL REFERENCES local_execution_runs(run_id),
  node_id TEXT NOT NULL,
  node_ordinal INTEGER NOT NULL CHECK(node_ordinal>=0),
  status TEXT NOT NULL CHECK(status IN ('pending','running','succeeded','failed','cancelled','skipped','stopped')),
  attempts INTEGER NOT NULL DEFAULT 0 CHECK(attempts>=0),
  max_attempts INTEGER NOT NULL CHECK(max_attempts>=1),
  display_name TEXT NOT NULL,
  role TEXT NOT NULL,
  output_json TEXT,
  output_digest TEXT,
  terminal_reason TEXT,
  PRIMARY KEY(run_id,node_id),
  UNIQUE(run_id,node_ordinal)
);

CREATE TABLE local_execution_attempts(
  attempt_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  node_id TEXT NOT NULL,
  attempt_number INTEGER NOT NULL CHECK(attempt_number>=1),
  status TEXT NOT NULL CHECK(status IN ('launched','succeeded','failed','validation_failed','cancelled')),
  assignment_json TEXT NOT NULL,
  assignment_digest TEXT NOT NULL,
  result_json TEXT,
  result_digest TEXT,
  failure_code TEXT,
  UNIQUE(run_id,node_id,attempt_number),
  FOREIGN KEY(run_id,node_id) REFERENCES local_execution_nodes(run_id,node_id)
);

CREATE TABLE local_execution_receipts(
  receipt_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES local_execution_runs(run_id),
  sequence INTEGER NOT NULL CHECK(sequence>=0),
  receipt_json TEXT NOT NULL,
  receipt_digest TEXT NOT NULL,
  UNIQUE(run_id,sequence),
  UNIQUE(run_id,receipt_digest)
);

