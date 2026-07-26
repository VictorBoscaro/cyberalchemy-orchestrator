# System Primitives

Normative candidate definitions for concrete primitives exposed by the system.

---

<a id="def-sys-001"></a>

## Label

- **ID:** DEF-SYS-001
- **Status:** candidate
- **Purpose:** Provide one lens through which an object can be classified.

### Definition

- **Domain:** A label is a named classification lens with exactly one value-selection mode:
  - **enumerated:** a finite value set that includes `other`;
  - **open:** values are selected according to a configurable prompt `R_L`.
- **Formal:** `mode(L) ∈ {enumerated, open}`. If `mode(L) = enumerated`, then
  `Values(L) = E_L` and `other ∈ E_L`. If `mode(L) = open`, then
  `Values(L) = {v | v is selected according to R_L}`.

### Relations

- **Domain:** A label admits the tags that may describe an object under its lens.
- **Formal:** `admits(L,t) ↔ t ∈ Values(L)`.

### Examples

- **Enumerated:** `purpose` admits `create`, `improve`, and `other`.
- **Open:** `research` uses `R_research` to select subjects materially treated by a research.

### Open questions

- Which parts of a label and its prompt constitute one versioned definition?

---

<a id="def-sys-002"></a>

## Tag

- **ID:** DEF-SYS-002
- **Status:** candidate
- **Purpose:** Express one answer under a label.

### Definition

- **Domain:** A tag is a value selected under a label.
- **Formal:** `tag_under(t,L) → t ∈ Values(L)`.

### Relations

- **Domain:** A tag describes an object under the lens of its label. How the tag was obtained is
  evidence about its use, not part of the tag value.
- **Formal:** `describes(o,L,t) → tag_under(t,L)`.

### Examples

- `improve` is a tag under the enumerated label `purpose`.
- `system-design` may be a tag under the open label `research`.

### Open questions

- Which labels are answered by agents, which are derived mechanically, and which admit both
  sources as distinct evidence?
- Is tag identity scoped to a label, or may one tag be shared by multiple labels?
