CREATE TABLE runtime_run_heads(
  run_id TEXT PRIMARY KEY REFERENCES runs(run_id),
  state TEXT NOT NULL CHECK(state IN (
    'confirmed','opening_pending','ready','running','execution_terminal',
    'close_pending','reconciliation_required','closed'
  )),
  version INTEGER NOT NULL CHECK(version>=1),
  last_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  last_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  opening_fence_status TEXT NOT NULL CHECK(opening_fence_status IN ('closed','verified')),
  opening_verification_event_id TEXT REFERENCES events(event_id),
  reconciliation_target TEXT CHECK(reconciliation_target IN ('opening','close')),
  CHECK(state='reconciliation_required' OR reconciliation_target IS NULL),
  CHECK(state!='reconciliation_required' OR reconciliation_target IS NOT NULL),
  CHECK(state NOT IN ('confirmed','opening_pending','reconciliation_required') OR opening_fence_status='closed'),
  CHECK(state NOT IN ('ready','running','execution_terminal','close_pending','closed') OR (
    opening_fence_status='verified' AND opening_verification_event_id IS NOT NULL
  ))
);

CREATE TABLE runtime_group_heads(
  graph_id TEXT NOT NULL REFERENCES confirmed_turn_graphs(graph_id),
  group_id TEXT NOT NULL,
  group_version INTEGER NOT NULL CHECK(group_version>=1),
  state TEXT NOT NULL CHECK(state IN (
    'pending','collecting','revealing','deliberating','voting','committing',
    'cancelling','completed','cancelled','failed'
  )),
  version INTEGER NOT NULL CHECK(version>=0),
  last_event_id TEXT UNIQUE REFERENCES events(event_id),
  last_offset INTEGER UNIQUE REFERENCES events(journal_offset),
  PRIMARY KEY(graph_id,group_id,group_version),
  CHECK((version=0)=(last_event_id IS NULL)),
  CHECK((last_event_id IS NULL)=(last_offset IS NULL))
);
