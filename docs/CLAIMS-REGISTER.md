# Claims register

**Why this file exists.** This system refuses to let a vendor claim become a fit
score without a basis tag. It would be incoherent to hold capability claims to
that standard and let its own founding narrative circulate untagged.

Every load-bearing factual claim in this repository is listed here with a status.
The rule is the same one the ruleset applies to itself: **an assertion whose
source cannot be produced is an assumption, and it is labelled as one.**

## Status vocabulary

| Status | Means |
|---|---|
| `SOURCED` | A specific, checkable source is named in this file |
| `AUTHOR-EXPERIENCE` | Drawn from the author's own engagement; not independently verifiable by a reader, and not a substitute for evidence |
| `UNVERIFIED` | Reported and believed, no source produced in this repository. **Treat as an assumption.** Do not quote to a regulator, an auditor, or a vendor negotiation |
| `ILLUSTRATIVE` | A worked example chosen to show a mechanism, not a report of a real event |

If you are preparing this material for an audience outside your own team, the
`UNVERIFIED` rows are the ones to either source or delete. They are persuasive,
which is exactly why they are dangerous.

---

## C1 — Platform availability was interrupted at a government customer in 2026

**Claim as used:** a vendor was pulled government-wide in February, switched off
at one department in March, and restored by injunction in April.

**Status:** `UNVERIFIED`

**Load-bearing for:** the entire continuity doctrine — `swap-warden`, the
`continuity_flags` block in the ruleset, the `watch` level on one platform, and
the continuity reserve as a budget line.

**Why it matters that it is unverified:** this claim currently sets a `watch`
flag on a named vendor, which is a commercially consequential statement about a
specific company. That is the highest-risk untagged claim in the repository.

**What would resolve it:** the docket number and the order, or a contemporaneous
report from a named outlet. Failing that, restate the doctrine on its logic
alone — availability is a contract variable — and drop the specific narrative.
The design conclusion does not actually depend on the anecdote.

---

## C2 — A production regulatory system was re-pointed to another vendor on ~72 hours' notice

**Claim as used:** the swap required re-engineering and revalidating a retrieval
pipeline; it sizes the continuity reserve and the swap-hours estimate.

**Status:** `UNVERIFIED`

**Load-bearing for:** `swap-warden`'s premise, `cost-modeler`'s continuity
reserve, `costmodel/assumptions.json`.

**What would resolve it:** name the organisation and the date, or relabel as
`ILLUSTRATIVE` and keep it as a scenario. As a scenario it still does its job:
it produces an estimate that a drill can then correct.

---

## C3 — Two published biomedical model comparisons twelve months apart inverted each other's rankings

**Claim as used:** the justification for principle 7 (no single-vendor
standardisation), for evidence expiry after two quarters, and for the
re-benchmark cadence being the durable asset.

**Status:** `UNVERIFIED`

**Load-bearing for:** `evals/rubric.md`, `eval-harness`, `DESIGN-PRINCIPLES.md`
principle 7, `AUDIT-READINESS.md` question 18.

**What would resolve it:** cite both studies. Until then the defensible version
of the argument is the one that does not need them: model rankings move with
version and licensed tier, both change on the vendor's schedule and not yours,
so a standardisation decision is a decision with an expiry date. That reasoning
stands on its own.

---

## C4 — The AI protein-design attribution critique

**Claim as used:** a widely-shared result was critiqued on the grounds that a
human wrote a ~16,000-word protocol, nearly two-thirds of it orchestration and
verification, with the molecular work done by specialist structural models — so
the language model's marginal contribution was never measured.

**Status:** `UNVERIFIED`

**Load-bearing for:** `evidence-auditor`'s founding template and attack 1
(attribution).

**Note:** the *method* — demand an ablation isolating the model from the
scaffold — is sound whether or not this specific critique is reported
accurately. Attack 1 survives deletion of the anecdote.

---

## C5 — Employees overstate AI usage to satisfy internal targets

**Claim as used:** the reason adoption counts are reported but never managed on.

**Status:** `UNVERIFIED`

**Load-bearing for:** `DESIGN-PRINCIPLES.md` principle 9, `/scorecard`.

**Note:** the design conclusion is independently defensible — a metric that is
cheap to inflate and that staff are rewarded for inflating is a bad control
variable, which is Goodhart's law and needs no survey behind it.

---

## C6 — Working biomedical researchers report over-refusal on legitimate work

**Claim as used:** the justification for `refusal-calibration` existing at all,
and for treating false-refusal rate as a first-class capability metric.

**Status:** `AUTHOR-EXPERIENCE` / `UNVERIFIED` as a rate

**Load-bearing for:** the `refusal-calibration` pack, the
`refusal-calibration` skill, `COMMUNITY-SIGNAL.md` signal 5, portfolio finding 3.

**Important distinction:** that the complaint is *made* is well attested in
practitioner discussion. That it is *true at a given rate for a given platform*
is exactly what the pack exists to measure and is currently unmeasured. Never
present the complaint as the measurement — that would be the failure this
repository is built to prevent, committed by the repository itself.

---

## C7 — A community-posted benchmark placed one coding stack ahead of another on bioinformatics tasks

**Claim as used:** context in a `fit` note.

**Status:** `UNVERIFIED`, single unreproduced source

**Handling:** the note already says single source, not independently reproduced,
not run on your code, `UNMEASURED HERE`. That is the correct treatment. It
informs no verdict and must not be upgraded without the seven attacks.

---

## C8 — The NIH GenAI Router case study

**Claim as used:** the structural source for this repository.

**Status:** `AUTHOR-EXPERIENCE` — Peter Kim, August 2026. The author's own prior
work, cited as such throughout.

---

## C9 — Every regulatory citation in the ruleset

**Status:** `SOURCED` but **not reconciled**. The `regulatory_anchors` block
names each instrument with a `confidence` field and, where relevant, a `verify`
instruction. These are starting points for reconciliation with counsel, not
legal advice, and `reconciliation_status` is `UNSIGNED`.

---

## C10 — Every cost figure

**Status:** `ILLUSTRATIVE`. `costmodel/assumptions.json` labels each rate
`PLACEHOLDER` with a basis string. No figure is a quote. The file exists so the
model re-runs the day a negotiated rate lands.

---

## Standing rule

A new doctrinal claim entering this repository gets a row here in the same
change. A claim with no row is not a claim; it is decoration, and
`evidence-auditor` should strike it.
