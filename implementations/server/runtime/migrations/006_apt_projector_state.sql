CREATE TABLE apt_projection_state(
  projection_name TEXT PRIMARY KEY,
  projector_version TEXT NOT NULL,
  apt_source_through_offset INTEGER NOT NULL CHECK(apt_source_through_offset>=0),
  source_through_offset INTEGER NOT NULL CHECK(source_through_offset>=0),
  updated_at TEXT NOT NULL
);
INSERT INTO apt_projection_state(
  projection_name,projector_version,apt_source_through_offset,
  source_through_offset,updated_at
) VALUES(
  'apt.granular','apt.granular-projector@1',0,0,
  strftime('%Y-%m-%dT%H:%M:%fZ','now')
);
