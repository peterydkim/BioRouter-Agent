# End-to-end workflows

Six documented workflows. Each names the trigger, the agents, the artifacts
produced, and the decision gate. These are the operational procedures an auditor
asks to see.

---

## W1 — Route a request (the core loop)

**Trigger:** scientist asks "can I use X for Y." **Target: under 60 seconds.**

```
scientist
   |
   v
intake-triage ........ tuple: work_type, data_class, jurisdiction, volume, destination
   |                   REFUSES pasted data. Max 3 clarifying rounds.
   v
route-advisor ........ freshness banner -> verdict -> rule -> fit + basis tag
   |                   -> approver + SLA -> continuity flag -> ranked alternatives
   +--> blocked? ----> escalation with 3 routes. COST MODEL OFF.
   +--> production? -> swap-warden (verified alternate?)
   +--> cost asked? -> cost-modeler
   |
   v
registry/intake-log.jsonl   (tuple + outcome only, never request text)
```

**Gate:** conditional verdicts do not proceed without the named approver.

**Failure mode to watch:** more than three clarifying rounds. That is a taxonomy
problem, not a user problem — log it as an open item.

---

## W2 — Convert an ASSUMED score to EVIDENCE

**Trigger:** quarterly cadence, new model version, or a disputed fit score.

```
credibility-assessment skill
   |  context of use -> influence x consequence -> model risk -> evidence bar
   v
eval-harness ......... pack exists? use it. else taskpack-authoring skill.
   |                   n>=5, versions pinned, scaffold constant across arms
   |                   zero-shot AND agentic reported separately
   v
evals/results/<pack>-<date>-<runid>.json
   |
   v
evidence-auditor ..... seven attacks: attribution, version drift, scaffold
   |                   asymmetry, n/spread, leakage, cherry-pick, consequence match
   |
   +--> PROMOTE ................. propose fit edit
   +--> PROMOTE NARROWED SCOPE .. promote named subset only
   +--> HOLD .................... fix named gap, re-run
   +--> DOWNGRADE ............... return to ASSUMED with reason
   |
   v
ruleset owner APPLIES the edit    <-- agents propose; only the owner applies
   |
   v
rulesets/CHANGELOG.md
```

**Gate:** `eval-harness` never edits its own evidence base. An agent that can
silently promote its own results is not an evidence base.

**Expiry:** EVIDENCE reverts to ASSUMED on model version change or after two
quarters, whichever comes first.

---

## W3 — Onboard a new use case to the portfolio

**Trigger:** a business unit proposes an AI use case not in the portfolio.

1. `portfolio-strategist` — place it on the value chain; derive influence,
   consequence, model risk. **Do not tier by subject matter.**
2. `intake-triage` — determine the data class, including *destination*.
3. `route-advisor` — permitted platforms at that class.
4. Evidence gap check — does a pack cover this context of use? If not, it is a
   pack-authoring task before production, not after.
5. `privacy-guardian` — DPIA trigger check if any personal data is in scope.
6. `cost-modeler` — TCO, only if a permitted path exists.
7. `swap-warden` — register with a verified alternate before production.

**Gate:** no production entry without (a) a permitted path, (b) an evidence
position stated with its tag, and (c) a registered alternate or an explicit
`NONE AVAILABLE` with a named risk owner.

---

## W4 — Model version change

**Trigger:** vendor ships a new version or announces a deprecation.

```
ruleset-reconciler ... is this a deprecation? get the EOL date
   |
   +--> expire affected EVIDENCE tags -> revert to ASSUMED
   +--> eval-harness: re-benchmark active packs on the new version
   |       INCLUDING refusal-calibration -- refusal boundaries move between
   |       versions and a workflow built on the old boundary breaks silently,
   |       with no error message
   +--> registry: find workflows pinned to the retiring version
   |       -> swap-warden with the EOL date attached
   +--> GxP-flagged workflows -> QA: requalification assessment
   |       a version change on a validated path IS a change-control event
   v
CHANGELOG entry + updated fit cells
```

**Gate:** GxP workflows do not move to a new version without QA sign-off.

---

## W5 — Continuity event

**Trigger:** a platform becomes unavailable, or terms change materially.

1. Query `registry/workflows.json`, order by blast radius.
2. Re-verify each alternate is ruleset-permitted **today** — the ruleset may have
   moved since the alternate was verified.
3. GxP-flagged workflows to QA first; longest lead time.
4. Execute swaps; record actual hours against estimate.
5. Correct the estimates afterward — a wrong drill estimate is the most valuable
   data the registry will ever collect.
6. `cost-modeler` draws on the continuity reserve; report actual versus reserved.

**Gate:** never swap a GxP path without revalidation.

---

## W6 — Quarterly governance cycle

**Trigger:** calendar.

| Step | Agent | Output |
|---|---|---|
| Reconcile ruleset | `ruleset-reconciler` | CHANGED / CONFIRMED / UNVERIFIABLE / OPEN ITEMS |
| Re-benchmark packs | `eval-harness` → `evidence-auditor` | Updated fit cells + expiries |
| Drill high-blast-radius workflows | `swap-warden` | Drill records with degradation notes |
| Refresh cost against actuals | `cost-modeler` | Variance report |
| Portfolio review | `portfolio-strategist` | Wave promotions/demotions |
| Publish scorecard | `/scorecard` | Six input metrics |
| Audit-pack refresh | `audit-liaison` | Evidence binder current |

**Gate:** if two or more stop-signals from `docs/OPERATING-CADENCE.md` are
present, the quarter's output is a rescope proposal rather than a status report.

---

## Agent interaction map

```
                    ┌─────────────────┐
                    │ portfolio-      │  where do we adopt, in what order
                    │ strategist      │
                    └────────┬────────┘
                             │
   scientist ──> intake-triage ──> route-advisor ──┬──> cost-modeler
                    (no data)      (reads ruleset) │    (refuses blocked)
                             │                     └──> swap-warden
                             │                          (alternate verified)
                    privacy-guardian
                    (DPIA, de-id, transfers)

   eval-harness ──> evidence-auditor ──> ruleset-reconciler ──> [OWNER APPLIES]
   (runs packs)     (7 attacks)          (versions, freshness)

                    audit-liaison
                    (answers from artifacts only; never improvises a control)
```

**Two invariants across every workflow:**

1. **Agents propose; the named owner applies.** Nothing in this system can
   change its own ruleset.
2. **No path prices a blocked verdict.** There is no override flag.
