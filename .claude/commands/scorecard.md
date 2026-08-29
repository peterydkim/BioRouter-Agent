---
description: Produce the program scorecard on the six managed input metrics, plus the reported lagging outputs.
argument-hint: [optional period, e.g. "Q3"]
---

Program scorecard. Period: **$ARGUMENTS** (current quarter if empty).

Read `registry/intake-log.jsonl`, `registry/workflows.json`,
`rulesets/ruleset.v1.json`, `rulesets/CHANGELOG.md`, and `evals/results/`.

Field map, so the metrics are computed and not estimated: coverage counts log
rows against known AI use cases; latency is the median of `latency_seconds`
(`resolved_at` − `received_at`); SLA attainment is `sla_met` over rows with a
non-null `approver_required`; evidence ratio is the `basis` distribution in the
ruleset's `fit` block; freshness is today minus `last_reconciled`; swap readiness
is the share of `workflows.json` entries with a non-null `last_drill_date` and a
`drill_result` other than `never-drilled`.

If a metric cannot be computed from these fields, report it as **not measured**
rather than estimating it. An estimated input metric is worse than a missing one,
because it looks like a measurement.

## Managed input metrics — these are the ones you move

| Metric | Source | Why it is the right thing to move |
|---|---|---|
| Share of new AI use cases entering through Router intake | intake-log | Coverage. An uncovered use case is an ungoverned one. |
| Median time from intake to a permitted path | intake-log | The actual customer experience. Weeks to minutes is the win. |
| Conditional cases with a named approver and a met SLA | intake-log + ruleset | Conditional cells are where tickets, drift and incidents originate. |
| Share of fit scores tagged EVIDENCE rather than ASSUMED | ruleset `fit` | Converts the recommendation from marketing inference into measured fact. |
| Days since last ruleset reconciliation | ruleset + CHANGELOG | A stale ruleset is worse than none, because it is trusted. |
| Production workflows with a documented, drilled alternate | workflows.json | Swap readiness. Continuity expressed as a number. |

## Lagging outputs — reported, not managed

Support tickets per hundred users, all-in cost per seat, shadow-AI incidents,
time-to-first-value.

## The metric this program refuses to manage on

**Adoption counts.** They are cheap to inflate and staff are rewarded for
inflating them, so they are a bad control variable. A program managed on adoption
gets adoption theatre. Report usage if asked; never set a target on it. (The
stronger claim that this is documented is C5 in `docs/CLAIMS-REGISTER.md`,
**UNVERIFIED** — do not cite it as evidence.)

Show the EVIDENCE-versus-ASSUMED ratio as the headline. At the start of a program
it will be near zero, and that is the honest number — say so rather than hiding
it. Moving it is what the evaluation harness is for.
