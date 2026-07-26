# Reference Scout bibliography research — collected returns

Date: 2026-07-25  
Dispatch: `2026-07-25-reference-scout-bibliography-research`  
Proposal: `plans/governed-agent-work-infrastructure/workstreams/reference-scout-bibliography-research-proposal.json`  
Launch-time proposal digest: `sha256:c73b22af31d276e97d09dd54ac77b72407b94763a17043c04868a0f0360ed9c8`  
Canonical feature location: `docs/features/agent-provenance-telemetry/research/reference-scout-bibliography/`

## Dispatch shape

Three independent seats examined different evidence surfaces. There were no
agent-to-agent connections and no seat received another seat's result.

| Seat | Role | Independent angle |
|---|---|---|
| Hewitt, Carl | explorer | Scholarly corpus and standards for provenance, bibliography, search reporting and evidence lineage |
| Liskov, Barbara | explorer | Operational research systems, retrieval pipelines, automatic collection and reproducible acquisition |
| Parnas, David | skeptic | Ownership, definitional soundness and unsupported-capability audit against the current repository |

The proposal passed independent capability, anti-bias/tension and containment
checks before launch. The existing lifecycle hooks managed each physical
subagent launch and close; this document does not create or replace ledger
records.

## Return A — scholarly and standards corpus

The scholarly explorer retained the following primary or official sources.

| Reference | Stable identifier or official locator | Constraint supported |
|---|---|---|
| W3C, *PROV-DM: The PROV Data Model* (2013) | [W3C Recommendation](https://www.w3.org/TR/2013/REC-prov-dm-20130430/) | Preserve entity, activity and agent identities and explicit attribution/derivation roles. |
| W3C, *Constraints of the PROV Data Model* (2013) | [W3C Recommendation](https://www.w3.org/TR/2013/REC-prov-constraints-20130430/) | Validate uniqueness, ordering and generation/use constraints instead of treating a provenance graph as unvalidated annotations. |
| Rethlefsen et al., *PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews* (2021) | [doi:10.1186/s13643-020-01542-z](https://doi.org/10.1186/s13643-020-01542-z) | Log source/platform, complete search strategy, date, limits, result count and deduplication. |
| DataCite Metadata Working Group, *DataCite Metadata Schema 4.6* (2024) | [doi:10.14454/mzv1-5b55](https://doi.org/10.14454/mzv1-5b55); [schema](https://schema.datacite.org/meta/kernel-4.6/) | Use structured creators, titles, publisher, dates, types, identifiers, related identifiers, versions, rights and language. |
| Crossref, *REST API documentation* | [Official documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | Crossref can supply canonical DOI metadata and query response metadata, but its response is provider evidence rather than proof that content was accessed. |
| ORCID, *ORCID API and record schema 3.0* | [Official documentation](https://info.orcid.org/documentation/integration-guide/orcid-record/) | Carry persistent contributor identifiers separately from display names. |
| Shotton, *CiTO, the Citation Typing Ontology* (2010) | [doi:10.1186/2041-1480-1-S1-S6](https://doi.org/10.1186/2041-1480-1-S1-S6) | Model why a source is related to a claim as a typed relation, separately from the fact that it was cited. |
| Wilkinson et al., *The FAIR Guiding Principles for scientific data management and stewardship* (2016) | [doi:10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18) | Favor globally unique identifiers, rich metadata, resolvable links and provenance suitable for reuse. |

The explorer's minimum logging recommendation was:

1. Search/run evidence: objective, source-policy snapshot, provider and adapter,
   exact query, timestamp, limits and filters, pagination, raw result count,
   deduplication procedure and outcome per channel.
2. Bibliographic description: title, creators and persistent contributor IDs,
   publication dates, container/publisher, resource type, identifiers, locator,
   version/relations, language, rights, metadata provider and retrieval time.
3. Acquisition observation: whether a result was only returned, opened, or its
   content was accessed; selector or anchor; response/content digest; actor;
   evaluation and rejection reason.
4. Delivery evidence: committed recommendation and bundle identities/digests,
   receipt or event position, target Attempt and resulting effective input.
5. Downstream APT semantics: declared use kind, typed claim relation and
   reference-check method/result, each bound to the relevant evidence rather
   than inferred from a locator.

## Return B — operational systems corpus

The systems explorer retained the following primary systems sources and
official interfaces.

| Reference | Stable identifier or official locator | Operational lesson |
|---|---|---|
| Nakano et al., *WebGPT: Browser-assisted question-answering with human feedback* (2021) | [arXiv:2112.09332](https://arxiv.org/abs/2112.09332) | A browser trajectory and quoted evidence can make web-assisted answers inspectable; a final citation alone does not reproduce acquisition. |
| Lála et al., *PaperQA: Retrieval-Augmented Generative Agent for Scientific Research* (2023) | [arXiv:2312.07559](https://arxiv.org/abs/2312.07559) | Scientific retrieval requires a pipeline for finding, parsing, ranking and citing documents, not just a model prompt. |
| Skarlinski et al., *Language agents achieve superhuman synthesis of scientific knowledge* / PaperQA2 (2024) | [arXiv:2409.13740](https://arxiv.org/abs/2409.13740) | Higher-quality synthesis depends on explicit literature search and evidence retrieval stages whose outputs can be evaluated independently. |
| Crossref, REST API | [Official documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | DOI lookup/search is automatable through a provider adapter with query, cursor, response and retry capture. |
| OpenAlex | [Priem, Piwowar and Orr, arXiv:2205.01833](https://arxiv.org/abs/2205.01833); [API docs](https://docs.openalex.org/) | Broad scholarly discovery and work/author/source identifiers are automatable, but must be reconciled with other identifier authorities. |
| Europe PMC, RESTful Web Service | [Official documentation](https://europepmc.org/RestfulWebService) | Biomedical metadata and, where licensed, full-text links can be queried through a dedicated adapter. |
| W3C PROV | [W3C Recommendation](https://www.w3.org/TR/prov-overview/) | Provider execution, retrieval and transformation should remain attributable activities with preserved entities and agents. |
| RO-Crate 1.2 | [doi:10.5281/zenodo.13751027](https://doi.org/10.5281/zenodo.13751027) | A portable research package can describe data, software, people, actions and contextual entities without replacing source-specific receipts. |
| ISO 28500:2017, WARC | [ISO standard page](https://www.iso.org/standard/68004.html) | HTTP request/response payloads and metadata need a stable archival container when replayable web evidence is required. |
| DataLad, `run` command | [Official documentation](https://docs.datalad.org/en/stable/generated/man/datalad-run.html) | Record command, inputs, outputs and resulting state when a retrieval/transformation step must be reproducible. |

Repository inspection led the explorer to this capability split:

### Operational in the local pilot

- A small, single-worker/single-reviewer Scout lifecycle.
- Append-before-ack publication, receipt verification, immutable accepted bundle,
  delivery to a target Attempt, retry handling and dispatch lineage.
- Exact repository reads can carry SHA-256, media type, byte size, event identity
  and journal position.
- Web or MCP acquisitions currently preserve only a locator and tool identity
  with `metadata_only` coverage.

### Not operationally established

- Generic provider launch or native MCP retrieval.
- A tensioned multi-seat Scout with reveal/review choreography.
- External-network or production authority.
- Cross-provider bibliographic identity reconciliation.
- Automatic query/pagination for Crossref, OpenAlex, Europe PMC or arXiv.
- License/open-access resolution and full-text acquisition.
- Request/response capture, content selectors, cursor/retry evidence or WARC
  packaging.
- Browser trajectories or a PaperQA-like retrieval and synthesis pipeline.

The systems explorer therefore classified those items as adapter or later
workflow work, not current Scout capability.

## Return C — ownership and definitional skeptic

The skeptic returned `FAIL pending boundary corrections`, with these blocking
observations:

1. The current pilot proves only the small Scout shape. `tensioned` and
   generalized multi-agent execution remain target design.
2. The runtime does not yet perform source acquisition or launch an external
   Scout provider merely because its schema can describe those concepts.
3. Desired bibliography fields are not present as an owned normalized record in
   the current migration/storage model.
4. ACI's recommendation `reference_id` is an opaque per-run identity, not a DOI
   authority or a deduplication key.
5. Scout-supplied `access_state` and locator data are recommendation payload;
   they are not trusted host `SourceObservation` evidence.
6. APT's `ResearchReferenceUse.reference_id` is explicitly opaque and “not
   bibliographic equivalence.”
7. `session_direct` is specified but the currently evidenced runtime path is
   dispatch-bound.
8. APT owns declared use, claim relation and checking semantics. It does not own
   acquisition/runtime truth.
9. No present owner was found for a normalized bibliography/catalog identity,
   its conflicts, or cross-provider merge decisions.
10. Any local design heuristic without a retained primary source must remain a
    hypothesis, not a research-backed rule.

The skeptic required the synthesis to retain four separate fact classes:

| Fact class | Current authority |
|---|---|
| Runtime lifecycle, accepted recommendation and target delivery | ACI |
| Mediated source acquisition/access actually observed | Host `SourceObservation` owner |
| Scout's proposed reference and metadata | Scout recommendation carried by ACI |
| Declared use, relation to a claim and support checking | APT |

A recommendation, delivery, observed access, declared use, claim relation and
support check must never be collapsed into one status.

## Parent acceptance check

| Check | Result |
|---|---|
| Independent source and systems angles preserved | PASS |
| Skeptic's boundary corrections applied | PASS |
| Current capability separated from proposed/adapted capability | PASS |
| ACI, host and APT authorities remain distinct | PASS |
| Sources are primary papers, standards or official documentation | PASS |
| Unsupported acquisition or access claims rejected | PASS |

Exit reason: `resolved`. The dispatch established a source-backed design
boundary and the next decision; it did not mutate either feature specification
or implement provider acquisition.
