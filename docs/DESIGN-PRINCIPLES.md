# Design principles

Read this before changing any agent definition. Each principle exists because
of a specific observed failure, and the failure is named.

---

## 1. Permission and capability never merge into one score

**Failure it prevents:** a platform scores "8/10 overall" and nobody can tell
whether it lost points for being legally restricted or for being bad at the task.
Those require opposite responses — one is a legal conversation, the other is an
engineering one.

**How it is enforced:** `route-advisor` renders verdict and fit in separate
fields and states plainly when the permitted platform is not the most capable
one. That gap is real information, not an embarrassment to smooth over.

## 2. Every capability claim carries a basis tag

**Failure it prevents:** a vendor claim becomes a fit score becomes a
recommendation becomes an architecture, and nobody remembers that step one was a
product page.

**How it is enforced:** the `fit` block stores `{score, basis, note}` and
`ASSUMED` renders to users as **"assumed, not tested."** `evidence-auditor` may
downgrade any tag at any time. Tags expire on model version change or after two
quarters.

**Honest starting state:** this ruleset ships with 55 `ASSUMED`, 5 `EXTERNAL`,
0 `EVIDENCE`. That is what an honest day-one fit table looks like. Moving that
ratio is the entire purpose of the harness.

## 3. Never price a path nobody may use

**Failure it prevents:** a cost estimate for a blocked path circulates, someone
budgets against it, and the program is now advocating for the workaround it was
built to prevent.

**How it is enforced:** `cost-modeler` hard-stops on `blocked` and there is no
override flag.

## 4. The router never receives the data

**Failure it prevents:** the governance tool becomes the highest-value target and
the most restricted system in the estate — it would inherit every restriction it
exists to route around.

**How it is enforced:** `intake-triage` refuses pasted content. The intake log
records the tuple and the outcome, **never the request text**, because request
text in a research organization is itself sensitive.

## 5. Conditional paths resolve to a named role and an SLA

**Failure it prevents:** "check with security" — which is not an answer, produces
no record, and after four days becomes whatever the scientist did last time.

**How it is enforced:** `approver_roles` carries a title and `sla_days`; every
conditional cell names one. SLA attainment is a managed input metric.

## 6. Freshness is displayed and tracked

**Failure it prevents:** a stale ruleset, which is worse than no ruleset because
it is trusted.

**How it is enforced:** `route-advisor` leads every answer with the freshness
banner and the signature status. `ruleset-reconciler` is explicitly forbidden
from touching `last_reconciled` without a real review — the single worst
available failure of this system is making stale look fresh.

## 7. No single-vendor standardization

**Failure it prevents:** a memo naming a winner, wrong within two quarters.
Rankings move with model version and licensed tier, both of which change on the
vendor's schedule rather than yours, so a standardisation decision carries an
expiry date it does not control. (The supporting anecdote about two published
comparisons inverting is claim C3 in `docs/CLAIMS-REGISTER.md`, **UNVERIFIED**.
The principle does not rest on it.)

**How it is enforced:** the durable assets are the re-benchmark cadence and the
swap protocol, and both are budget lines. `swap-warden` gates production entry on
a verified alternate.

## 8. Adversarial review of your own evidence

**Failure it prevents:** the program's own benchmarks become marketing for the
program. The failure mode is subtle and self-serving: you ran a real evaluation,
so the number feels earned, and nobody asks what fraction of the result was the
scaffold rather than the model.

**How it is enforced:** `evidence-auditor` runs seven attacks and applies them
*symmetrically* — evidence that flatters the incumbent gets the same treatment as
evidence that threatens it, and evidence produced by this program gets the
harshest treatment of all. "Not measured" is a complete and frequently correct
output.

## 9. Managed on inputs, reported on outputs

**Failure it prevents:** adoption theatre. Adoption counts are cheap to inflate
and staff are rewarded for inflating them, which makes them a bad control
variable — Goodhart, and no survey needed. (The stronger claim that employees
demonstrably overstate AI usage against internal targets is C5 in
`docs/CLAIMS-REGISTER.md`, **UNVERIFIED**.)

**How it is enforced:** `/scorecard` leads with six input metrics — coverage,
latency, SLA attainment, evidence ratio, ruleset freshness, swap readiness — and
reports lagging outputs without setting targets on them.

## 10. A service, not a gate

**Failure it prevents:** the tool that gets routed around. Every blocked answer
that ends without a route is a request that migrates to a personal account.

**How it is enforced:** blocked verdicts return three concrete routes — reduce
the class, relocate the work, or open a named exception. Latency and coverage are
measured; blocks are not. If the headline metric is "requests denied," the design
has already failed.

---

## The load-bearing insight

> Nobody needs a fifth model. They need to know which of the four they already have.

The scarce asset is not model access. It is a **maintained answer with an owner**.
Everything in this repository is downstream of that sentence, and any change that
makes the answer less maintained, or its ownership less clear, is a regression
regardless of what else it improves.
