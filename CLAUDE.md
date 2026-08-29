# BioRouter — operating charter

**Status: design sketch. Not tested, not reviewed, not validated.** No security,
privacy, QA, legal or export reviewer has signed the matrix; no capability score
has been measured; no pack has been run against a real model; no cost figure is a
quote. The code has tests and CI, which says the harness works — not that any
verdict is right. Nothing here should drive a real routing, compliance or
purchasing decision.

A governed routing and evaluation layer over the generative AI platforms a
biotech or pharmaceutical company **already licenses**. It answers one question
for a working scientist:

> For this piece of work, on this data, which platform am I permitted to use,
> how good is it actually at this, what does it cost, and who signs when the
> answer is conditional?

Adapted from the NIH GenAI Router case study (Peter Kim, August 2026). The NIH
version routed across CHIRP, ChatGPT Enterprise, Gemini, Claude and M365 Copilot
under NIH/HHS policy. This version routes across a commercial platform estate
under FDA / EMA / GxP / HIPAA / GDPR / export-control constraints.

---

## The seven rules. These are not style preferences.

**1. Permission and capability are different questions and never merge into one
score.** Permission comes from policy and is binary-ish (permitted / conditional
/ blocked). Capability fit is a 1–5 score on a use case. A platform can be fully
permitted and bad at the task. Reporting one number hides which one you are
looking at.

**2. Every capability score carries a basis tag.**
- `EVIDENCE` — a local harness run against a named task pack, with a run ID and a date.
- `EXTERNAL` — a published head-to-head study, cited.
- `ASSUMED` — an inference from vendor documentation. Not measured.

Never present `ASSUMED` without the tag. Treating an assumption as a measurement
is the most common way an enterprise AI rollout goes wrong. The job of the
evaluation harness is to convert `ASSUMED` into `EVIDENCE`, one task pack at a time.

**3. Never price a path nobody may use.** If the verdict is `blocked`, the cost
model switches off and the output is an escalation with a named role. Putting a
number on an unauthorized path is how a governance tool becomes a liability.

**4. The router never receives the data. Only its classification.** A governance
tool that ingests what it governs inherits every restriction it is trying to
route around. Users describe the data class; they never paste the data.

**5. Every conditional path resolves to a named role and an SLA, never an inbox.**
Conditional cells are where tickets, drift and incidents originate. An unrouted
"no" is exactly the request that becomes shadow AI on a personal account.

**6. The ruleset is a versioned artifact with a displayed freshness date and one
named owner.** If the date is stale, the answer should be distrusted, and
freshness is a tracked metric rather than a background chore. A routing layer
with distributed ownership degrades into a wiki page nobody trusts in two quarters.

**7. Do not standardize on a single vendor.** Published comparisons invert
themselves inside twelve months, and the licensed tier moves the score as much
as the vendor does. The durable assets are the **re-benchmark cadence** and the
**swap protocol**, which is why revalidation and a continuity reserve are budget
lines and not afterthoughts.

---

## What this system explicitly does not do

- It does not build, fine-tune, or host a model.
- It does not grant authority. It surfaces authorizations that already exist, or
  states that none does.
- It does not touch PHI, PII, trade secret, or export-controlled material.
- It does not produce clinical decision support, diagnostic output, or a
  regulatory conclusion. Work is routed and costed, never interpreted.
- It does not name an enterprise-wide winner. That is the question the evidence
  says to stop asking.

---

## Repository map

| Path | What it is | Who edits it |
|---|---|---|
| `rulesets/ruleset.v1.json` | The permission matrix: platforms x data classes, with the rule cite and approver for every cell. **The core maintained asset.** | Router owner, countersigned by Security/QA |
| `rulesets/CHANGELOG.md` | Version history and reconciliation dates | Router owner |
| `evals/taskpacks/*.json` | Domain task packs that produce `EVIDENCE` scores | Evaluation engineer |
| `evals/rubric.md` | Scoring rules, variance handling, promotion thresholds | Evaluation engineer |
| `evals/run_eval.py` | Zero-dependency harness runner | Evaluation engineer |
| `costmodel/assumptions.json` | Every rate, visible and editable. No figure here is a quote. | Router owner + Finance |
| `registry/workflows.json` | Production workflows and their verified alternate platform | Router owner + workflow owners |
| `docs/` | Design principles, the NIH-to-industry mapping, operating cadence | Router owner |
| `docs/CLAIMS-REGISTER.md` | Every doctrinal claim this repo makes, with its status. Seven are UNVERIFIED. **Read before repeating any of them.** | Router owner |
| `tools/validate.py`, `tools/test_scorers.py` | The invariants that are controls rather than norms. Run in CI on every push. | Eval engineer |

## Agents

Run `/route`, `/evaluate`, `/reconcile`, `/cost`, `/swap-drill`, `/scorecard`,
`/portfolio`, `/audit`, `/dpia`. Agent definitions live in `.claude/agents/` and
the skills they load live in `.claude/skills/`. Read
`docs/DESIGN-PRINCIPLES.md` before changing any of them.

## House style for anything this system emits

State the rule and its date next to the answer. Name the role that signs, not a
team. Say "assumed" out loud when it is assumed. Prefer being told which part
reads wrong over being told it was interesting.

This applies to the system's own claims too. A doctrinal assertion with no row in
`docs/CLAIMS-REGISTER.md` is decoration, and an absence of measurement is never
reported as a zero.
