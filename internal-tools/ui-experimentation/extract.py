#!/usr/bin/env python3
"""
extract.py — read the append-only dispatch ledger and emit a clean, self-contained
JSON of ONLY the dispatches that have real graph STRUCTURE, for the standalone HTML
viewers under ui-experimentation/.

A dispatch is "structured" (worth inspecting) if any group has >= 2 agents, OR
contains a reviewer/skeptic/auditor role, OR the dispatch declares `connections`.
Trivial single-agent-no-edge dispatches are filtered OUT.

Full initial_prompt and angle text are preserved verbatim — those are the payoff
that gets clicked to reveal.

Run:  python extract.py
Out:  data/dispatches.json
"""
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LEDGER = os.path.join(REPO, "telemetry", "agents", "subagents-dispatch.yaml")
OUT = os.path.join(HERE, "data", "dispatches.json")

REVIEWER_ROLES = {"reviewer", "skeptic", "auditor"}


def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def load_json_col(v):
    """groups/connections may be a JSON string or already-parsed list."""
    if v is None:
        return []
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return []
        return json.loads(s)
    return v


def is_structured(groups, connections):
    if connections:
        return True
    for g in groups:
        agents = as_list(g.get("agents"))
        if len(agents) >= 2:
            return True
        for a in agents:
            if (a.get("role") or "").lower() in REVIEWER_ROLES:
                return True
        # explicit intra-group connections field, if any
        if g.get("connections"):
            return True
    return False


def structure_score(d):
    """Richness heuristic for picking the best corpus."""
    agents = sum(len(as_list(g.get("agents"))) for g in d["groups"])
    edges = len(d.get("connections", []))
    reviewers = sum(
        1
        for g in d["groups"]
        for a in as_list(g.get("agents"))
        if (a.get("role") or "").lower() in REVIEWER_ROLES
    )
    prompt_chars = sum(
        len(a.get("initial_prompt") or "") + len(a.get("angle") or "")
        for g in d["groups"]
        for a in as_list(g.get("agents"))
    )
    return (agents * 3) + (edges * 5) + (reviewers * 4) + (prompt_chars / 2000.0)


def clean_agent(a):
    return {
        "agent_name": a.get("agent_name"),
        "role": a.get("role"),
        "model": a.get("model"),
        "token_budget": a.get("token_budget"),
        "angle": a.get("angle"),
        "initial_prompt": a.get("initial_prompt"),
    }


def clean_group(g):
    return {
        "group_id": g.get("group_id"),
        "n": g.get("n"),
        "anti_bias": g.get("anti_bias"),
        "robot_talks": g.get("robot_talks"),
        "agents": [clean_agent(a) for a in as_list(g.get("agents"))],
    }


def main():
    with open(LEDGER, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    rows = doc.get("dispatches", [])
    # collect close rows to attach exit_reason / agents_spawned
    closes = {}
    for r in rows:
        if "close_of" in r:
            closes[r["close_of"]] = {
                "exit_reason": r.get("exit_reason"),
                "agents_spawned": r.get("agents_spawned"),
                "feedback_prompts": r.get("feedback_prompts"),
            }

    structured = []
    for r in rows:
        if "close_of" in r or "dispatch_id" not in r:
            continue
        groups = load_json_col(r.get("groups"))
        connections = load_json_col(r.get("connections"))
        if not is_structured(groups, connections):
            continue
        d = {
            "dispatch_id": r["dispatch_id"],
            "dispatch_type": r.get("dispatch_type"),
            "created": r.get("created"),
            "goal": r.get("goal"),
            "context": r.get("context"),
            "anti_bias_global": r.get("anti_bias_global"),
            "max_loops": r.get("max_loops"),
            "working_folder": r.get("working_folder"),
            "groups": [clean_group(g) for g in groups],
            "connections": connections,
            "close": closes.get(r["dispatch_id"]),
        }
        d["_score"] = round(structure_score(d), 2)
        structured.append(d)

    structured.sort(key=lambda d: d["_score"], reverse=True)

    # Pick the richest 4-8 as the corpus.
    corpus = structured[:8]
    if len(corpus) < 4:
        corpus = structured  # keep whatever we have

    payload = {
        "generated_from": "telemetry/agents/subagents-dispatch.yaml",
        "selection": "structured dispatches only (>=2 agents OR reviewer/skeptic/auditor OR connections)",
        "total_structured_found": len(structured),
        "corpus_size": len(corpus),
        "dispatches": corpus,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # Also emit a JS wrapper so the standalone HTML works from file:// (browsers
    # block fetch() of a local .json). The .json stays the canonical source; this
    # is a pure double-click-to-view fallback loaded via <script src>.
    js_out = os.path.join(HERE, "data", "dispatches.js")
    with open(js_out, "w", encoding="utf-8") as f:
        f.write("// AUTO-GENERATED by extract.py — file:// fallback for dispatches.json.\n")
        f.write("// Canonical source is dispatches.json; do not hand-edit.\n")
        f.write("window.__DISPATCHES__ = ")
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write(";\n")

    print(f"structured found: {len(structured)}")
    print(f"corpus written : {len(corpus)} -> {OUT}")
    for d in corpus:
        agents = sum(len(g["agents"]) for g in d["groups"])
        print(f"  {d['_score']:>6}  {agents}a {len(d['connections'])}e  {d['dispatch_id']}")


if __name__ == "__main__":
    sys.exit(main())
