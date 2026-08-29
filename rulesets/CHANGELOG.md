# Ruleset changelog

Every change records: date, version, cells touched, source, reviewer, signature
status. Semantic versioning — patch for a citation refresh, minor for a verdict
change, major for a taxonomy change.

**A verdict change without a named human reviewer is not a reconciliation. It is
an edit, and it must be labelled as one.**

---

## 2.1.0-draft — 2026-08-29

**Status: UNSIGNED.** **This is an edit, not a reconciliation.** `last_reconciled`
stays at 2026-08-24; no source was walked.

Minor bump. No verdict changed and no class was added or removed. Two corrections
that came out of an adversarial review of this repository, both of which made the
system's own numbers look worse and its statements truer.

### 1. Five `EXTERNAL` fit tags downgraded to `ASSUMED`

`imaging` and `lit` cells on the three commercial platforms asserted that
published head-to-head comparisons exist, and named none. `evals/rubric.md`
defines `EXTERNAL` as **a cited published study**, so an uncited pointer at a
literature is an inference wearing a citation's authority — precisely the failure
basis tags exist to prevent, committed in the shipped ruleset.

- **Fit basis distribution: 60 ASSUMED, 0 EXTERNAL, 0 EVIDENCE** (was 55/5/0).
- `tools/validate.py` now fails the build on an `EXTERNAL` tag with no
  `citation` field, and on an `EVIDENCE` tag with no run id, run date, or
  matching file in `evals/results/`. The rule is now a control rather than a norm.
- Restoring an `EXTERNAL` tag requires a specific study, its date, and the
  statement that it was not run on this company's work.

### 2. `germline-seq` scoped to prompt content

The class as first written classified **subject matter**, which over-blocked
badly: "which GATK flag restricts calling to one gene" contains no sequence, but
would have routed to a class where four platforms are blocked. A class that
blocks most genomics questions does not protect sequence data, it relocates the
work to a personal account.

Added `classification_scope` to the ruleset as the governing text, and three
boundaries on the class:

- **It classifies what enters the prompt**, plus destination. Pipeline
  configuration, parameter choice, tool comparison and error interpretation route
  at `research-unpub` or `public`.
- **Somatic is in scope where the germline travels with it.** A tumour-normal
  pair contains a germline sample by construction; a tumour-only call set carries
  unfiltered germline variants. The first version covered germline only, which
  left the commonest oncology configuration falling back to `clin-deid` — the
  class that handles sequence badly and the reason `germline-seq` was created.
- **Public, openly consented reference resources are not escalated.** The
  escalate-when-arguable rule reaches ambiguity about your own data, never
  published reference data.

Verdicts unchanged: 78 cells, 37 permitted, 20 conditional, 21 blocked.

### Also in this change, outside the ruleset

- `docs/CLAIMS-REGISTER.md` — every doctrinal claim in the repository tagged.
  Ten entries, of which **seven are UNVERIFIED**, including the vendor
  availability narrative that sets a `watch` continuity flag on a named company.
  Holding capability claims to a basis standard while the founding narrative
  circulates untagged was a double standard an external reviewer would find
  quickly.
- `tools/validate.py` and `tools/test_scorers.py`, run in CI. Six evaluation
  scorers were fixed, including two hard-negative items that scored the correct
  answer 0.0 and the hallucination 1.0.
- `registry/intake-log.jsonl` created with timestamps. Coverage and latency —
  two of the six managed input metrics — were previously unmeasurable because
  the file did not exist and the schema had no start or end time.

**Open items unchanged at nine.** Nothing here answers #9 or #10; the scope fix
narrows what they apply to without resolving either.

---

## 2.0.0-draft — 2026-08-29

**Status: UNSIGNED.** No security, privacy, QA or legal review has occurred.
**This is an edit, not a reconciliation.** `last_reconciled` is deliberately left
at 2026-08-24: no source was walked, so refreshing the freshness stamp would make
a stale ruleset look fresh, which is the worst available failure of this system.
The file keeps the name `ruleset.v1.json` so that existing agent and doc
references do not break; the version is carried in `ruleset_version`.

**Major bump — taxonomy change.** Closes open item #8.

### Added: `germline-seq` (tier 7)

Human germline sequence — raw reads, genotypes and variant calls on identifiable
or re-identifiable individuals.

- **Reviewer:** none. Derived from public regulatory text, as in 1.0.0-draft.
- **Source:** HIPAA §164.514 (the eighteen Safe Harbor identifiers, which do not
  reach sequence data — a recognised gap in the rule rather than a permission);
  GDPR Article 9, which names genetic data explicitly; the NIH controlled-access
  genomic access model as the structural analog.
- **Cells added:** 6. `enclave` and `gxp` conditional on the Privacy Officer,
  four commercial platforms blocked.
- **Verdict distribution:** 78 cells — 37 permitted, 20 conditional, 21 blocked.
- **Fit basis distribution:** unchanged at 55 ASSUMED, 5 EXTERNAL, 0 EVIDENCE.
  `fit` is keyed by use case rather than by data class, so a taxonomy change does
  not touch it.

**The load-bearing consequence: there is no self-service route to this class on
any platform.** Every germline cell is conditional or blocked. That is not an
oversight to be corrected in the next pass — it is the point. Authorisation for
germline sequence attaches to the named investigator and the approved research
use, not to the infrastructure, so containment alone never produces a
`permitted` verdict here. `clin-deid` handled this badly precisely because it
allowed one.

**What changes for routing.** Work that previously classified as `clin-deid`
because the sequence "had the identifiers stripped" now classifies as
`germline-seq`, and four platforms that were conditional for it are blocked.
Affects portfolio use cases 10, 11, 22 and 30 — the genomics spine. Anyone
holding a `clin-deid` verdict on sequence work should re-route.

**Tier placement is itself a judgement.** Tier 7: above `clin-deid` because the
identifiers cannot be removed, below `clin-id` only because a sequence without a
linked clinical record needs an external reference panel to attribute. If your
consent forms or your Data Use Agreements treat sequence as identifiable on its
face, this belongs at tier 8. Recorded as open item #10 rather than asserted.

### Open items — updated

| # | Status |
|---|---|
| 8 | **CLOSED** by this version. The class exists. The questions it was standing in for do not close with it — see #9 and #10. |

| # | Cell(s) | Question | Owner | Due |
|---|---|---|---|---|
| 9 | `enclave`, `gxp` × `germline-seq` | Which germline datasets carry consent, Data Use Agreement or Data Use Certification terms that permit processing by a hosted model **at all**, including inside our own enclave? Containment does not answer this and the conditional verdicts assume an answer nobody has produced. The genomics-specific instance of #1, and it inherits its priority. | Legal + DPO | Day 45 |
| 10 | `germline-seq` tier and attenuation | Two questions. Does this belong at tier 7 or tier 8 — do our consent forms treat sequence as identifiable on its face? And is there an accepted aggregation (allele counts, cohort frequencies) that genuinely lowers the class, at what cohort size, determined by whom? Requesters will ask for this route immediately and it must not be answered ad hoc. | DPO + genomics lead | Day 60 |

Register now stands at **nine open items**: #1–#7 carried forward unchanged,
#8 closed, #9 and #10 added.

---

## 1.0.0-draft — 2026-08-24

**Status: UNSIGNED.** No security, privacy, QA or legal review has occurred.

Initial construction. 72 cells across 6 platforms and 12 data classes, derived
from public regulatory text and from the structure of the NIH GenAI Router case
study (Peter Kim, August 2026).

- **Reviewer:** none
- **Source:** public regulatory text only; see `regulatory_anchors` in the ruleset
- **Verdict distribution:** 37 permitted, 18 conditional, 17 blocked
- **Fit basis distribution:** 55 ASSUMED, 5 EXTERNAL, 0 EVIDENCE

### Open items — cells nobody can currently answer

These are unverifiable from outside the company. They are the first ninety days
of work, and they are recorded here rather than guessed.

| # | Cell(s) | Question | Owner | Due |
|---|---|---|---|---|
| 1 | All commercial × `clin-deid` | Which DUAs, CRO MSAs and clinical trial agreements carry non-transferability clauses, and do any of them reach model prompting? **This is the highest-value open item in the register** — it is the direct analog of the NIH controlled-access rule and the cell most likely to be wrong. | Legal | Day 45 |
| 2 | All commercial × `cci`, `predec` | Actual contracted retention windows, training exclusions and subprocessor lists per vendor. Marketing pages are not contracts. | Procurement / Legal | Day 30 |
| 3 | `enclave` × `gxp-record` | Has any enclave been qualified for a GxP context of use, or is the conditional verdict theoretical? | QA CSV | Day 60 |
| 4 | `enclave` × `export-durc` | Does the deemed-export analysis for enclave access by foreign nationals exist? Who performed it? | Empowered Official | Day 60 |
| 5 | All × jurisdiction | The matrix currently has no jurisdiction axis. If EU or UK subjects are in scope, several `clin-deid` cells likely need to split by jurisdiction. | DPO | Day 45 |
| 6 | `copilot` × `research-unpub` | What actually lives in the tenant today? The conditional verdict assumes tenant contents are correctly classified, which is rarely true at first inspection. | IT / Records | Day 30 |
| 7 | All `fit` cells | Every capability score is ASSUMED or EXTERNAL. None has been measured on this company's work. | Eval engineering | Day 90 for the first pack |
| 8 | **Missing class: human germline sequence** | The taxonomy has no class for raw human sequence data, and `clin-deid` handles it badly. Genomic sequence is **re-identifying in its own right**: HIPAA Safe Harbor's 18 identifiers do not list sequence data (a known gap), while GDPR Art. 9 names genetic data explicitly. So the same dataset can be "de-identified" under one regime and special-category personal data under the other. This is the closest structural analog to NIH's controlled-access genomic rule and it is currently unrepresented. Raised 2026-08-24 by an NGS variant-calling routing request. | DPO + Legal | Day 45 |

### Known weaknesses, stated rather than discovered later

- **No jurisdiction axis.** See open item 5. This is the most likely structural
  change in v2.
- **The `enclave` platform is underspecified.** Its capability depends entirely on
  which weights are hosted, and the fit scores treat it as one thing when it is a
  category.
- **`pv` and `gxp-record` fit scores are near-meaningless** because the only
  permitted platform has never been measured. High-consequence contexts of use
  with unmeasured capability are the worst combination in the table, and they
  should be first in the evaluation queue rather than last.
