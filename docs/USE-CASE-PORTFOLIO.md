# AI use-case portfolio across the pharma R&D value chain

**Purpose.** Answer the executive question — *where do we adopt first, and why
that order* — with the same discipline the router applies to a single request:
permission and capability scored separately, model risk derived rather than
asserted, and every claim carrying its basis.

**Audience.** R&D leadership, digital/IT governance, QA, Privacy, and the
stakeholders who will audit this.

**Status.** Risk tiers are derived from the credibility-assessment framework and
are defensible. Data classes and permitted platforms trace to
`rulesets/ruleset.v1.json`, which is **UNSIGNED**. Value estimates are judgement,
labelled as such. No capability claim here is `EVIDENCE`.

---

## How to read the tiering

**Model risk = model influence × decision consequence.** Not "how scary does the
topic sound." A model drafting a CSR section that four people review has *lower
influence* than a model silently choosing a variant-calling parameter, even
though the CSR sounds more consequential.

This is the distinction that most pharma AI portfolios get wrong: they tier by
*subject matter* and end up over-governing literature search while
under-governing pipeline configuration.

| Risk | Evidence bar before production |
|---|---|
| **Low** | n≥5, one pack, ASSUMED acceptable if tagged |
| **Medium** | n≥5, domain pack, variance reported, evidence-auditor review |
| **High** | n≥10, held-out pack, domain reviewer, ablation isolating model from scaffold, acceptance criteria pre-registered |
| **High + GxP** | All of the above, plus QA involvement, version pinning under change control, revalidation trigger on version change |

---

## Wave 1 — adopt now (0–6 months)

Low-to-medium risk, high volume, permitted on commercial platforms for the
common data classes. These fund the program's credibility.

| # | Use case | Stage | Influence | Consequence | Risk | Data class | Permitted | Evidence bar |
|---|---|---|---|---|---|---|---|---|
| 1 | Literature & evidence synthesis for target rationale | Discovery | Low | Medium | **Low-Med** | `public` | All | `literature-grounding` |
| 2 | Competitive/patent landscape monitoring | Discovery/BD | Low | Medium | **Low-Med** | `public`,`cci` | All | `literature-grounding` |
| 3 | Analysis code assist — Python/R/Nextflow | Discovery | **High** | Medium | **Medium** | `research-unpub` | All 4 scientific | `bioinformatics-code` |
| 4 | Assay & lab protocol drafting | Discovery | Low | Low | **Low** | `research-unpub` | All 4 scientific | Light |
| 5 | Internal meeting/document productivity | Enabling | Low | Low | **Low** | `internal` | Copilot (native) | None |
| 6 | Regulatory intelligence monitoring | Regulatory | Low | Medium | **Low-Med** | `public` | All | `literature-grounding` |
| 7 | Medical information response drafting | Med Affairs | Low | Medium | **Medium** | `public`,`cci` | All | `literature-grounding` |
| 8 | Publication & abstract drafting support | Med Affairs | Low | Low | **Low** | `research-unpub` | All 4 scientific | Light |

**Why these first.** Every one is permitted on platforms you already license, at
data classes that need no approver. Time-to-value is days. Note #3 is *Medium*
risk despite being "just coding" — silent parameter errors propagate, which is
exactly why `bioinformatics-code` and `variant-calling` exist.

---

## Wave 2 — build toward (6–18 months)

Medium risk, higher value, and most require either the enclave or a named
approver. This is where the evaluation harness earns its budget.

| # | Use case | Stage | Influence | Consequence | Risk | Data class | Permitted | Evidence bar |
|---|---|---|---|---|---|---|---|---|
| 9 | Single-cell / bulk omics interpretation | Discovery | Med | Medium | **Medium** | `research-unpub` | All 4 scientific | `omics-interpretation` |
| 10 | Variant calling pipeline construction & triage | Genomics | **High** | Med-High | **High** | `research-unpub` or `germline-seq`* | Enclave; commercial cond.* | `variant-calling`, n≥10 |
| 11 | Target safety & genetic association review | Discovery | Med | **High** | **High** | `public`,`research-unpub` | All 4 scientific | `omics` + `literature` |
| 12 | Cheminformatics pipeline code (RDKit, docking triage) | Hit/Lead | **High** | Medium | **Medium** | `ts-chem` | Enclave; commercial cond. | New pack needed |
| 13 | SAR summarisation & med-chem synthesis | Lead Op | Med | Medium | **Medium** | `ts-chem` | Enclave preferred | New pack needed |
| 14 | Toxicology literature & risk assessment support | Preclinical | Med | **High** | **High** | `research-unpub` | All 4 scientific | `refusal-calibration` critical |
| 15 | PK/PD & biomarker modelling code | Translational | **High** | Medium | **Medium** | `research-unpub` | All 4 scientific | `bioinformatics-code` |
| 16 | Imaging analysis pipeline code | Translational | **High** | Medium | **Medium** | `research-unpub` | All 4 scientific | New pack needed |
| 17 | Clinical protocol & synopsis drafting | Clinical | Low-Med | **High** | **High** | `cci` | All 4 scientific | `regulatory-writing` |
| 18 | Informed consent drafting & readability | Clinical | Med | **High** | **High** | `cci` | All 4 scientific | `regulatory-writing` |
| 19 | Site feasibility & selection analytics | Clinical | Med | Medium | **Medium** | `cci` | All 4 scientific | New pack needed |
| 20 | ELN/lab data extraction & structuring | Discovery | **High** | Medium | **Medium** | `research-unpub` | Enclave preferred | New pack needed |
| 21 | CMC deviation investigation drafting | CMC | Med | **High** | **High** | `cci` → `gxp-record` | Depends on destination | `regulatory-writing` |

*The `germline-seq` class was added in ruleset `2.0.0-draft` and scoped in
`2.1.0-draft` (2026-08-29), closing open item #8. It classifies **what enters the
prompt**, not the subject matter: where human sequence is pasted or attached, the
commercial platforms are **blocked**, not conditional, and the enclave route is
conditional on the Privacy Officer. Pipeline and parameter work on the same study
puts no sequence in the prompt and routes at `research-unpub` — so use case 10 is
not blocked as a whole, and reading it that way is the error the scope rule
exists to prevent.

**Why this wave is the real program.** Nine of these thirteen need either an
evidence pack that does not exist yet or an approver decision. That is the work.

---

## Wave 3 — the high-value, high-bar tier (18 months+)

These carry the largest value and the strictest evidence requirements. Several
have **exactly one permitted platform** and therefore no swap alternate.

| # | Use case | Stage | Influence | Consequence | Risk | Data class | Permitted | Blocker |
|---|---|---|---|---|---|---|---|---|
| 22 | Clinical data programming (SDTM/ADaM) | Clinical | **High** | **High** | **High+GxP** | `clin-deid` | Enclave, GxP inst. | Validation |
| 23 | CSR drafting | Clinical | Med | **High** | **High+GxP** | `gxp-record` | **GxP instance only** | No alternate |
| 24 | Submission module drafting (M2) | Regulatory | Med | **High** | **High+GxP** | `gxp-record` | **GxP instance only** | No alternate |
| 25 | Health authority question response | Regulatory | Med | **High** | **High+GxP** | `gxp-record` | **GxP instance only** | No alternate |
| 26 | ICSR narrative drafting & coding | PV | **High** | **High** | **High+GxP** | `pv` | **GxP instance only** | QPPV sign-off |
| 27 | Signal detection literature screening | PV | Med | **High** | **High** | `pv`,`public` | GxP; public tier open | QPPV sign-off |
| 28 | Aggregate safety report drafting (PBRER) | PV | Med | **High** | **High+GxP** | `pv` | **GxP instance only** | QPPV sign-off |
| 29 | Medical monitoring narrative support | Clinical | Med | **High** | **High+GxP** | `clin-deid`/`clin-id` | Enclave cond.; GxP | DPIA |
| 30 | Patient–trial matching support | Clinical | **High** | **High** | **High** | `clin-id` | Enclave conditional | DPIA + lawful basis |

---

## Four findings that should change your investment decision

### 1. The enclave is the single highest-leverage infrastructure decision

Count the rows. **The private research enclave is permitted at data classes where
all three commercial platforms are conditional or blocked** — `clin-deid`,
`ts-chem`, and (conditionally) `clin-id`. Roughly half of Wave 2 and Wave 3
either unlocks or de-risks on enclave availability.

The strategic read: buying more commercial seats does not open new use cases past
a certain point. **Enclave capacity does.** If there is one capital ask in this
portfolio, it is that.

The counterweight is honest: enclave capability fit is 2–3/5 across the board
versus 4/5 for frontier commercial models, because it depends entirely on which
weights you host. **You are trading capability for permission.** That trade is
correct for `clin-deid` and wrong for public literature work, and the router
exists so nobody has to guess which case they are in.

### 2. Your highest-value use cases have no swap alternate

Use cases 23–28 have exactly one permitted platform: the validated GxP instance.
`registry/workflows.json` honestly records `alternate_platform: NONE AVAILABLE`
rather than naming a blocked commercial platform to fill the field.

This is a **real, open, unmitigated continuity risk** on the most business-critical
tier. Mitigation is a second qualified instance or a documented manual fallback.
Both cost money. Both belong in the budget conversation rather than in a risk
register nobody reads.

### 3. Refusal calibration is a portfolio-level risk, not a curiosity

Use cases 14 (toxicology), 11 (target safety), 26–28 (safety/PV) all sit in
vocabulary that triggers model safety filters. A platform with a high
false-refusal rate on toxicology is **unusable for an entire portfolio segment**,
regardless of its coding scores.

No vendor publishes this number. It is measurable in a week and it can eliminate
a platform from a whole tier. Run it before the next licensing decision, not after.

### 4. Sequence by evidence-bar reachability, not by value

The instinctive move is to start with the highest-value use cases. Those are
Wave 3, they need the highest evidence bar, and they will stall for eighteen
months while the program's credibility burns.

Wave 1 is not the "easy stuff." It is how you build the evidence machine, the
intake habit, and the approver relationships that make Wave 3 possible at all.
**A program that starts at CSR drafting never gets to CSR drafting.**

---

## What is missing, stated plainly

- **Four use cases need packs that do not exist**: cheminformatics, imaging
  pipelines, site feasibility, ELN extraction. Until then their fit scores are
  `ASSUMED` and should be presented as such in any business case.
- **No use case here has an `EVIDENCE` tag.** Zero. Every capability
  statement is inference.
- **Value estimates are judgement, not modelled.** No NPV, no time-savings
  study. Anyone presenting this as quantified benefit is overstating it.
- **The germline sequence class now exists** (ruleset `2.0.0-draft`, scoped in
  `2.1.0-draft`), which narrows routing for use cases 10, 11, 22 and 30 — the
  genomics spine — **for the steps that put sequence in the prompt**. There is no
  self-service route to that class on any platform. What remains open is whether
  consent and Data Use Certification terms permit model processing at all (open
  item #9) and whether any aggregation lowers the class (#10). Neither is
  answerable from outside the company.
- **No capability claim in this portfolio carries a citation any more.** Five
  cells were tagged `EXTERNAL` on the strength of a literature that was never
  cited; they were downgraded to `ASSUMED` on 2026-08-29. The fit table is now
  60 `ASSUMED`, 0 `EXTERNAL`, 0 `EVIDENCE` — a worse-looking number and a truer
  one.
