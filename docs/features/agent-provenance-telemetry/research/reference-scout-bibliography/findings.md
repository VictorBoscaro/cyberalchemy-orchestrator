# Reference Scout bibliography research — findings

Date: 2026-07-25  
Status: accepted synthesis  
Dispatch: `2026-07-25-reference-scout-bibliography-research`
Canonical owner folder: `docs/features/agent-provenance-telemetry/research/`

## Answer

The Scout can already recommend and deliver opaque references through ACI, but
it cannot yet claim to have built a verified bibliography. A real bibliography
requires provider adapters, host-observed acquisition evidence and one
explicitly owned normalized bibliographic record. ACI should continue to own
the run and delivery; the host should continue to own observed access; APT
should continue to own downstream use and claim semantics.

## What exists and what does not

| Capability | Current status | Authority |
|---|---|---|
| Small Scout run, worker/reviewer lifecycle | Implemented local pilot | ACI |
| Accepted recommendation and immutable bundle | Implemented local pilot | ACI |
| Delivery into one target Attempt/effective input | Implemented local pilot | ACI |
| Exact local-file digest/size/media evidence | Implemented for the bounded path | Host/runtime evidence carried by ACI |
| Web/MCP locator and tool name | Available only as `metadata_only` | Recommendation/acquisition metadata; not proof of content access |
| Trusted source access observation | Contract boundary exists; general implementation is later | Host `SourceObservation` |
| Declared citation/use, claim relation and checking | Specified downstream semantics | APT |
| Tensioned multi-seat Scout | Proposed, not current runtime capability | Future ACI profile |
| Provider search, pagination and retry capture | Missing adapter | Future provider adapter under ACI orchestration |
| DOI/ORCID/other identifier reconciliation | No current owner or implementation | Decision required |
| Normalized bibliography record and conflict policy | Absent | Decision required |
| Full-text/license resolution, selectors and response archive | Missing adapter/host observation path | Provider adapter + host |

## Recommended ownership decision

Introduce a separately named bibliographic authority rather than overloading
either existing opaque `reference_id`.

Preferred placement:

1. APT owns a new `BibliographicReferenceRecord` research entity and its
   normalization/conflict policy because canonical bibliographic identity is
   research-domain semantics.
2. ACI keeps `ScoutRecommendation.reference_id` opaque and may carry an optional
   immutable `bibliographic_record_ref` plus record digest. ACI transports that
   reference; it does not normalize or merge it.
3. The host remains the sole owner of `SourceObservation`, including whether a
   result was returned, opened or content-accessed and the exact coverage and
   evidence digest.
4. `ResearchReferenceUse` remains an attributed use of a reference in one
   research result. Its existing opaque `reference_id` must not silently become
   the canonical DOI/deduplication identity.

This is a recommendation, not an already-settled specification. It needs a
decision gate because the alternative—an independent bibliography/catalog
capability referenced by both ACI and APT—is also coherent if bibliography
normalization will serve domains beyond research provenance.

## Minimum bibliographic profile

A normalized record should distinguish asserted values from provider
observations and retain:

| Area | Minimum fields |
|---|---|
| Record identity | immutable record ID, schema version, record digest |
| Work identity | DOI and other identifiers with identifier type and normalized value |
| Description | title, resource type, container, publisher, language |
| Responsibility | ordered creators/contributors, display name, optional ORCID and role |
| Dates/version | issued/published dates, version, related identifiers with relation type |
| Access and rights description | public locator, rights/license metadata as reported by its source |
| Provider evidence | provider, retrieval time, exact query/lookup, response digest, source record ID/version |
| Reconciliation | candidate matches, deterministic normalization result, conflicts retained, decision rule/version |

No field in this record proves access. Access proof comes only from a bound host
observation.

## Minimum acquisition log

Each provider adapter run should record:

- objective and source-policy version;
- provider, adapter and adapter version;
- exact query or identifier lookup;
- timestamp, filters, limits, pagination/cursor and retry sequence;
- result count before and after deduplication;
- raw response digest and, when replay is required, an immutable response/WARC
  reference;
- per-result provider identity, stable locator and normalized-record candidate;
- outcome `returned`, `opened` or `content_accessed`, but only when the host
  actually observed that operation;
- selector/anchor and content digest for evidence extracted from accessed
  content;
- rejection or conflict reason;
- recommendation, accepted bundle, delivery receipt and target Attempt
  identities.

PRISMA-S constrains the search-reporting portion; DataCite, Crossref and ORCID
constrain metadata shape; W3C PROV constrains attribution and derivation; CiTO
informs typed claim relations; WARC/RO-Crate/DataLad offer packaging and
reproducibility precedents. None replaces the repository's owner-specific
receipts.

## Evidence verdicts

| Candidate assertion | Sound? | Required witness | Use mode |
|---|---|---|---|
| “The Scout recommended this locator.” | Yes today | ACI accepted recommendation/bundle | Runtime fact |
| “This recommendation reached the target Attempt.” | Yes today | ACI delivery event/receipt and effective-input binding | Runtime fact |
| “The Scout searched Crossref with this exact query.” | Not without adapter evidence | Provider adapter request/response receipt | Future runtime fact |
| “The content at this URL was accessed.” | Not from locator/tool metadata | Bound host `SourceObservation` | Host observation |
| “These two provider results describe the same work.” | Not without normalization authority | Versioned reconciliation rule and retained conflicts | Bibliographic semantic fact |
| “The research cited or consulted this work.” | Yes only when explicitly captured | APT `ResearchReferenceUse` with extraction evidence | Research semantic fact |
| “This work supports/refutes this claim.” | Yes only after relation/check evidence | APT claim relation and `ReferenceCheck` | Epistemic assessment |

## Specification and implementation sequence

1. Run a decision gate for the owner of normalized bibliographic identity:
   APT-local `BibliographicReferenceRecord` (preferred) versus an independent
   shared bibliography/catalog capability.
2. Update APT discovery/specification with the chosen record, provider assertion
   and conflict semantics; explicitly preserve the opaque meaning of the
   existing `ResearchReferenceUse.reference_id`.
3. Update ACI only with the transport/reference mapping, adapter execution
   receipts and delivery fields it actually owns. Keep host
   `SourceObservation` external.
4. Specify one narrow provider-adapter experiment—preferably Crossref plus
   OpenAlex reconciliation—with preregistered success/failure criteria for
   query replay, response digests, pagination, retry and identifier conflicts.
5. Implement only after the DomainSpec work pack, test specification and
   readiness receipt bind the exact brownfield scope.

No feature specification was changed by this research dispatch. Its result is
the evidence and ownership decision needed before those mutations are safe.

## Source index

- [W3C PROV-DM](https://www.w3.org/TR/2013/REC-prov-dm-20130430/)
- [W3C PROV Constraints](https://www.w3.org/TR/2013/REC-prov-constraints-20130430/)
- [PRISMA-S, doi:10.1186/s13643-020-01542-z](https://doi.org/10.1186/s13643-020-01542-z)
- [DataCite Metadata Schema 4.6, doi:10.14454/mzv1-5b55](https://doi.org/10.14454/mzv1-5b55)
- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [ORCID record/API documentation](https://info.orcid.org/documentation/integration-guide/orcid-record/)
- [CiTO, doi:10.1186/2041-1480-1-S1-S6](https://doi.org/10.1186/2041-1480-1-S1-S6)
- [FAIR principles, doi:10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)
- [WebGPT, arXiv:2112.09332](https://arxiv.org/abs/2112.09332)
- [PaperQA, arXiv:2312.07559](https://arxiv.org/abs/2312.07559)
- [PaperQA2, arXiv:2409.13740](https://arxiv.org/abs/2409.13740)
- [OpenAlex paper, arXiv:2205.01833](https://arxiv.org/abs/2205.01833)
- [Europe PMC REST API](https://europepmc.org/RestfulWebService)
- [RO-Crate 1.2, doi:10.5281/zenodo.13751027](https://doi.org/10.5281/zenodo.13751027)
- [ISO 28500:2017 WARC](https://www.iso.org/standard/68004.html)
- [DataLad `run`](https://docs.datalad.org/en/stable/generated/man/datalad-run.html)
