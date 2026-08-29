# Operating cadence

What runs when, who owns it, and what makes it fail.

## Fixed cadence

| Cadence | Activity | Agent | Owner |
|---|---|---|---|
| Continuous | Intake and routing | `intake-triage`, `route-advisor` | Product owner |
| Weekly | Open-items register review; conditional-path SLA check | `ruleset-reconciler` | Product owner |
| Monthly | Cost model refresh against actual consumption | `cost-modeler` | Product owner + Finance |
| Quarterly | Full ruleset reconciliation | `ruleset-reconciler` | Product owner + Security/Legal |
| Quarterly | Re-benchmark active packs | `eval-harness` → `evidence-auditor` | Eval engineer |
| Quarterly | Swap drills, high-blast-radius workflows | `swap-warden` | Workflow owners |
| Semi-annual | Swap drills, remaining workflows | `swap-warden` | Workflow owners |
| Semi-annual | Task pack refresh and leakage review | `eval-harness` | Eval engineer + domain reviewers |

## Event triggers — these outrank the calendar

| Event | Triggers |
|---|---|
| New model version ships | Re-benchmark; check pinned workflows; GxP paths → requalification assessment |
| Vendor announces a deprecation | Reconcile; find pinned workflows; hand to `swap-warden` **with the EOL date** |
| Platform becomes unavailable | `swap-drill` event mode, ordered by blast radius |
| Regulation or guidance changes | Targeted reconciliation of affected cells |
| **A contract is signed, renewed, or lapses** | Reconciliation — contracts set more cells than regulations do |
| Enterprise agreement renewal opens | Cost model with low/expected/high scenarios |
| A scientist reports being blocked on legitimate work | Refusal-calibration run; possible routing change |
| Any incident involving an unmanaged tool | Root-cause into intake coverage, not into user discipline |

## The first ninety days

Adapted from the case study. Note that days 1–30 build nothing.

**Days 1–30 · Orient and baseline.** Meet the people who already own pieces of
this: Security, Privacy, QA, Legal, the export officer, and whoever already
built an internal AI tool in a corner of R&D. Inventory every existing
deployment, including the ones nobody sanctioned. Baseline the support queue and
the current time-to-first-value. Begin reconciliation of the v1 ruleset. **Build
nothing.**

**Days 31–60 · Reconcile and publish.** Walk the matrix line by line with one
security officer and one legal reviewer until **someone signs** for one business
unit. Publish through a channel that already has an owner and an audit trail —
the existing intranet, the existing knowledge base — rather than standing up a
new system that needs its own approval. Mark every cell with a confidence level
and keep the unanswerable ones as an open-items register.

**Days 61–90 · Measure and hand over.** Sample thirty days of AI-related tickets
and count how many ask *which platform am I allowed to use* — a number nobody
currently holds, and the one that sizes the problem. Write the maintenance
procedure with a review trigger, a freshness target and a named owner. Run the
first real evaluation pack and convert at least one `ASSUMED` cell to `EVIDENCE`.
Give a written recommendation on whether a real application is worth the cost of
building one.

## The three failure modes, and the mitigation for each

**1. The ruleset goes stale and people stop trusting it.**
Mitigation: freshness is a displayed, tracked metric; reconciliation runs on a
fixed cadence rather than as-needed; the reconciler is forbidden from refreshing
the date without an actual review.

**2. It is perceived as a gate, so people route around it.**
Mitigation: measure latency and coverage, never blocks. Every conditional path
carries a named approver and an SLA. Blocked answers return three concrete routes
rather than a refusal. If your headline metric is "requests denied," you have
already lost.

**3. It is read as a procurement recommendation and gets pulled into a vendor
fight.** Mitigation: vendor-neutral by construction. Cost assumptions visible and
editable. The tool declines to price an unauthorized path. No enterprise-wide
winner is ever named.

## What would tell you to stop

Decide this in advance, and write the number down:

- Intake coverage stays flat while AI usage grows — scientists are routing around it.
- Median time-to-path does not beat the email path — you added a step.
- The EVIDENCE-versus-ASSUMED ratio does not move in two quarters — the harness
  is not real and the fit scores are marketing.
- Conditional-path SLAs are consistently missed — you built a queue, not a router.

Any two of these together is a signal to stop and rescope rather than to push
harder on adoption.
