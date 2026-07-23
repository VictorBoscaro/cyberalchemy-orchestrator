CREATE TABLE apt_research_captures_projection(
  research_capture_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL,
  expected_contribution_id TEXT NOT NULL,
  capture_status TEXT NOT NULL CHECK(capture_status IN ('captured','partial','missing')),
  raw_artifact_id TEXT,
  capture_digest TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  accepted_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  is_current INTEGER NOT NULL CHECK(is_current IN (0,1))
);
CREATE UNIQUE INDEX one_current_apt_capture_projection_per_contribution
ON apt_research_captures_projection(dispatch_id,expected_contribution_id)
WHERE is_current=1;

CREATE TABLE apt_research_facts_projection(
  fact_id TEXT PRIMARY KEY,
  research_capture_id TEXT NOT NULL REFERENCES apt_research_captures_projection(research_capture_id),
  subject_id TEXT NOT NULL,
  fact_kind TEXT NOT NULL CHECK(fact_kind IN (
    'research_question','research_answer','reference_use','research_problem',
    'research_claim','formalization_candidate'
  )),
  supersedes_fact_id TEXT REFERENCES apt_research_facts_projection(fact_id),
  payload_json TEXT NOT NULL,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  accepted_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  is_current INTEGER NOT NULL CHECK(is_current IN (0,1))
);
CREATE UNIQUE INDEX one_current_apt_projection_fact_per_subject
ON apt_research_facts_projection(research_capture_id,subject_id) WHERE is_current=1;

CREATE TABLE apt_research_questions_projection(
  research_question_id TEXT PRIMARY KEY,
  fact_id TEXT NOT NULL UNIQUE REFERENCES apt_research_facts_projection(fact_id),
  research_capture_id TEXT NOT NULL,
  question_text TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
CREATE TABLE apt_research_answers_projection(
  research_answer_id TEXT PRIMARY KEY,
  fact_id TEXT NOT NULL UNIQUE REFERENCES apt_research_facts_projection(fact_id),
  research_capture_id TEXT NOT NULL,
  question_ids_json TEXT NOT NULL,
  artifact_id TEXT NOT NULL,
  selector_json TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
CREATE TABLE apt_reference_uses_projection(
  reference_use_id TEXT PRIMARY KEY,
  fact_id TEXT NOT NULL UNIQUE REFERENCES apt_research_facts_projection(fact_id),
  research_capture_id TEXT NOT NULL,
  reference_id TEXT NOT NULL,
  reference_kind TEXT NOT NULL,
  locator_observed TEXT NOT NULL,
  use_kind TEXT NOT NULL,
  probe_recommendation_ref_json TEXT,
  payload_json TEXT NOT NULL
);
CREATE TABLE apt_research_problems_projection(
  problem_id TEXT PRIMARY KEY,
  fact_id TEXT NOT NULL UNIQUE REFERENCES apt_research_facts_projection(fact_id),
  research_capture_id TEXT NOT NULL,
  problem_kind TEXT NOT NULL,
  statement TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
CREATE TABLE apt_research_claims_projection(
  research_claim_id TEXT PRIMARY KEY,
  fact_id TEXT NOT NULL UNIQUE REFERENCES apt_research_facts_projection(fact_id),
  research_capture_id TEXT NOT NULL,
  statement TEXT NOT NULL,
  answer_ids_json TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
CREATE TABLE apt_formalizations_projection(
  formalization_id TEXT PRIMARY KEY,
  fact_id TEXT NOT NULL UNIQUE REFERENCES apt_research_facts_projection(fact_id),
  research_capture_id TEXT NOT NULL,
  research_claim_id TEXT NOT NULL,
  notation TEXT NOT NULL,
  latex TEXT,
  legend_json TEXT NOT NULL,
  reading TEXT NOT NULL,
  logic_family TEXT NOT NULL,
  assumptions_json TEXT NOT NULL,
  scope TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
CREATE TABLE apt_reference_lineage_projection(
  delivery_subject_key TEXT PRIMARY KEY,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  accepted_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  payload_json TEXT NOT NULL
);
