# Community signal — demand evidence, and what to do with it

## Epistemic status, stated first

The source material is public social-media discussion from biomedical
researchers, 2025 through August 2026: NIH-affiliated PIs, bioinformatics tool
authors, immunologists, academic power users, and vendor amplification accounts.

The originating NIH case study took this position, and it is retained:

> *"Social-media material reviewed during preparation was treated as directional
> signal only and is not cited, because it could not be independently verified."*

That stance is correct and it is also the reason this document is useful. **This
material is not evidence about model capability. It is evidence about
practitioner demand, workflow shape, and where trust breaks.** Those are
different claims with different verification requirements, and conflating them is
exactly the failure `evidence-auditor` exists to catch.

**Known biases, load-bearing:**
- **Engagement-selected.** The highest-reach posts are vendor-adjacent
  announcements. Sober negative results do not go viral.
- **Non-representative.** Federal employees face public-commentary constraints,
  so direct NIH-scientist volume is thin and skews to a few identifiable voices.
- **Self-reported.** No controlled comparison, no version pinning, no n.
- **Recency-unstable.** Model versions named here will be superseded within two
  quarters. The rankings will not survive; the *workflow patterns* will.

**Therefore:** nothing in this document may enter `rulesets/ruleset.v1.json` as
`EXTERNAL`. Community claims enter as **hypotheses with a named test**, or they
do not enter.

---

## Signal 1 — Adoption is already multi-model, and nobody is waiting

Working scientists mix platforms by task: one stack for coding, another for
literature and long-document work, a third for office and ecosystem integration.
This is observable across every account sampled, and it happens with or without a
governance layer.

**Implication:** the single-vendor standardisation question is already settled in
practice by user behaviour. A program that tries to reverse it will be routed
around. This is the strongest confirmation of Rule 7 in the charter, and it is
demand evidence rather than capability evidence — which makes it usable.

**Action:** none needed. The router is built on this premise.

---

## Signal 2 — Agentic/CLI tooling has displaced chat for real work

Repeated pattern: pure chat interfaces are treated as insufficient for pipelines
and multi-file work; the CLI and agent surfaces are where the work happens. One
academic advises colleagues to abandon browser chat entirely in favour of the
coding agent. Another describes the coding agent as the first application opened
each morning and the only one running continuously.

**Implication for evaluation:** benchmarking chat-surface performance measures
the wrong thing. This is why `evals/rubric.md` requires zero-shot and agentic to
be reported **separately** and the scaffold held constant across arms.

**Implication for governance:** agentic surfaces run tools, touch filesystems and
consume orders of magnitude more tokens. The cost model's warning that agentic
usage is the volatile line traces directly to this pattern.

**Action:** already reflected in the harness and cost model. Confirm the estate's
seat mix covers CLI/agent surfaces, not just chat licences.

---

## Signal 3 — A specific, testable bioinformatics coding claim

A bioinformatics tool author (ShinyGO/iDEP lineage — squarely the computational
biology community) posted a direct comparison: one vendor's coding stack at 93.8%
versus another's at 91% on a bioinformatics coding benchmark, with a strongly
worded preference. A separate widely-followed immunologist reports the same
directional preference for daily coding work.

**Status: single-source, unreproduced, unpinned as to scaffold, not run on your
code.** A ~3-point gap with no reported variance is not a finding — it is within
the range that repeat-to-repeat noise produces at small n.

**Hypothesis H1:** *Vendor A's coding stack outperforms Vendor B's on
domain-specific bioinformatics code generation.*

**Test:** `evals/taskpacks/bioinformatics-code.json`, n≥5, versions pinned,
scaffold constant. The pack deliberately weights **R and Nextflow** because the
community claim concerns bioinformatics specifically, and R/Nextflow are
under-represented in the public benchmarks such claims usually rest on.

**Decision it would change:** which platform is recommended for portfolio use
cases 3, 10, 12, 15, 16 — the coding spine of the whole portfolio.

---

## Signal 4 — Literature grounding: the strongest claim and the sharpest critique

Positive: a cell-biology PI and beta tester describes literature-connector
integration as transformative — *"like having a supercharged research
assistant"* — with claims of eliminated fabrication. Amplification posts describe
large scientific skill libraries covering drug discovery, single-cell analysis
and variant annotation pipelines.

Negative, and more useful: a genomics/AI practitioner argued about a widely-shared
protein-design result that a human wrote a 16,000-word protocol, nearly two-thirds
of it orchestration and verification, with the molecular work done by specialist
structural models — concluding that **the marginal contribution of the language
model itself had not been measured.** Separately, a researcher reports colleagues
in biology and hardware finding model-run analysis *"too surface level"* and
unable to *"search comprehensively."*

**These two are not in conflict.** They are consistent with a system that works
well because of its scaffolding, evaluated in a way that does not separate the
scaffold from the model.

**Hypothesis H2:** *Reported literature-grounding quality is substantially
attributable to retrieval scaffolding rather than to model capability.*

**Test:** `evals/taskpacks/literature-grounding.json`, run **with and without
connectors, same model, same items**. The delta is the finding. Also carries the
`fabricated-probe` item — a fictitious paper the model should fail to locate —
which directly tests the "no hallucinations" claim.

**Decision it would change:** whether the estate is buying a *model* or an
*integration*. If the delta is large, connector availability outranks model
choice, and the procurement conversation changes shape entirely.

**Note:** this critique became `evidence-auditor`'s founding template. It is the
single most valuable item in the whole corpus — and it is logged as claim **C4,
UNVERIFIED**, in `docs/CLAIMS-REGISTER.md`. The method it illustrates (demand an
ablation isolating model from scaffold) stands whether or not the anecdote is
reported accurately. Do not repeat the specifics as established fact.

---

## Signal 5 — Over-refusal on legitimate biomedical work

Consistent, cross-vendor complaint: safety filters declining or degrading
legitimate work on pathogens, toxicology, oncology and longevity. Researchers in
dual-use-adjacent areas report this as a workflow blocker rather than an
annoyance.

Claim **C6** in `docs/CLAIMS-REGISTER.md`. That the complaint is *made* is well
attested; that it is *true at a given rate for a given platform* is unmeasured,
and conflating the two would be this repository committing the exact error it
exists to prevent.

**This is the highest-value signal in the corpus**, because it is (a) directly
measurable, (b) unpublished by any vendor, (c) absent from every public
leaderboard, and (d) capable of eliminating a platform from an entire portfolio
tier — see portfolio use cases 11, 14, 26–28.

**Hypothesis H3:** *Platforms differ materially in false-refusal rate on
legitimate biomedical tasks, and the difference is large enough to change routing.*

**Test:** `evals/taskpacks/refusal-calibration.json`. Measured in both directions
and reported as a pair — a model that refuses everything scores perfectly on one
axis and is useless.

**Decision it would change:** platform recommendation for the entire
safety/toxicology/PV segment, and the next licensing negotiation.

---

## Signal 6 — Zero-shot accuracy is poor; agentic planning changes the picture

Referenced in the corpus: a benchmark of proprietary and open models on real
biomedical analysis tasks drawn from papers showed overall accuracy **below 40%
without iterative agentic planning**, rising substantially with agents.

**Implication:** any capability number quoted without stating the scaffold is
uninterpretable. A vendor quoting the agentic number and a skeptic quoting the
zero-shot number are both accurate and neither is informative.

**Action:** already binding in `evals/rubric.md` — report both conditions
separately, always.

---

## Signal 7 — "Model capability is not governance"

A practitioner's observation about deploying models into clinical workflows: a
general-purpose model does not possess the current clinical protocols, and
deploying one into a workflow is a governance act rather than a tooling choice.

**Implication:** this is the thesis of the entire system, arrived at
independently by a practitioner. Worth quoting to executive stakeholders who ask
why a routing layer is needed when the models are already licensed.

---

## Signal 8 — Vendor availability and access are political, not just technical

Reported internal conflict at a major lab over equalising AI tool access, where
the proposed resolution was removal for everyone and engineers objected strongly
enough to threaten departure. Alongside the documented 2026 federal
withdrawal-and-restoration sequence.

**Implication:** platform availability is a contract and politics variable, not
an engineering constant. Reinforces `swap-warden` and the continuity reserve.

---

## Summary — signal to test to decision

| # | Signal | Hypothesis | Pack | Decision it changes |
|---|---|---|---|---|
| 1 | Multi-model in practice | — | — | Confirms Rule 7; no test needed |
| 2 | Agentic > chat for real work | — | Scaffold discipline | Seat mix; cost model |
| 3 | Coding stack A > B on bioinformatics | H1 | `bioinformatics-code` | Coding platform for use cases 3, 10, 12, 15, 16 |
| 4 | Literature grounding: model vs scaffold | H2 | `literature-grounding` + ablation | Are we buying a model or an integration |
| 5 | Over-refusal on biomedical work | H3 | `refusal-calibration` | Platform for use cases 11, 14, 26–28 |
| 6 | Zero-shot poor, agentic better | — | Rubric rule | How every number is reported |
| 7 | Capability ≠ governance | — | — | Executive framing |
| 8 | Availability is political | — | Swap drills | Continuity reserve |

**Three hypotheses, three existing packs, zero results.** That is the honest
state. The corpus told us precisely what to measure and nothing about what the
answer is.

---

## What this document deliberately does not do

- **Name individuals as evidence sources in the ruleset.** Handles and quotes
  informed hypothesis selection. They do not appear in `regulatory_anchors` or in
  any `fit` cell.
- **Treat vendor amplification as capability data.** The highest-reach posts in
  the corpus are announcement amplification, and reach is not validity.
- **Assume the named model versions remain current.** They will not. The
  hypotheses are durable; the version names in them are not.
- **Substitute for a structured instrument.** The right replacement for scraped
  social signal is a quarterly structured survey of your own scientists, with
  known denominators. That is a program deliverable, and this document is the
  placeholder until it exists.
