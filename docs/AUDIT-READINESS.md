# Audit readiness

For QA audits, health authority inspection, partner due diligence, and the
internal review that decides whether this program continues.

**Operating stance:** an auditor should learn every weakness of this system from
us, in writing, before they find it. The open-items register exists for that
purpose. A program that discloses its gaps is credible; a program whose gaps are
discovered is finished.

---

## Evidence binder — question to artifact

| Auditor question | Artifact | Owner |
|---|---|---|
| What decides which AI platform may be used? | `rulesets/ruleset.v1.json` | Router owner |
| Who approved that ruleset? | `rulesets/CHANGELOG.md` — **currently UNSIGNED** | Router owner |
| How do you know it is current? | `last_reconciled` + freshness metric on `/scorecard` | Router owner |
| What happens when it is stale? | Distrust banner on every answer past target | Router owner |
| Who signs a conditional case? | `approver_roles`, role + SLA on every conditional cell | Named approvers |
| How do you know a model is fit for a task? | `evals/` — run ID, date, pack, variance | Eval engineer |
| How do you prevent marketing claims becoming policy? | Basis tags + `evidence-auditor` seven attacks | Eval engineer |
| Does the tool process personal data? | No. Class only. `docs/DATA-GOVERNANCE.md` | Privacy |
| How is a GxP context handled? | Validated instance only; change control on version | QA |
| What if a vendor becomes unavailable? | `registry/workflows.json` + drill records | Workflow owners |
| How do you know people use it? | Intake coverage on `/scorecard` | Router owner |
| What are the known gaps? | `rulesets/CHANGELOG.md` open items — **9 logged** | Router owner |
| Where do your own factual claims come from? | `docs/CLAIMS-REGISTER.md` — every doctrinal claim tagged, UNVERIFIED ones named | Router owner |
| How do you know the tool obeys its own rules? | `tools/validate.py` + `tools/test_scorers.py`, run in CI | Router owner |

---

## The twenty questions a top-20 pharma stakeholder will actually ask

Answers written to be given verbatim.

**1. Is this a validated system?**
No, and it does not need to be. It processes no GxP record and no personal data —
it returns a policy lookup. Validation attaches to the *platforms* it routes to,
and the validated GxP instance is the only one qualified for GxP records.

**2. You are recommending AI models. Who is accountable if one is wrong?**
The sponsor. Accountability does not transfer to a vendor or a model. The router
surfaces authorisations that already exist and never grants authority.

**3. Your capability scores — where do they come from?**
Today, all 60 from vendor documentation and inference (`ASSUMED`), **0 from
measurement**. Five were previously tagged `EXTERNAL`; we downgraded them on
2026-08-29 because they pointed at a literature without citing a study, and our
own rubric defines `EXTERNAL` as cited. Every score is tagged, and `ASSUMED`
renders to users as "assumed, not tested." Converting them is the harness's job.

**4. So you are making recommendations on unmeasured claims?**
We are making *permission* decisions on policy and *capability* observations on
tagged inference, and we never merge the two into one score. A user is told
explicitly when a fit score is untested. That is a better position than a single
blended number whose provenance nobody can reconstruct.

**5. Who owns the ruleset?**
One named person, currently UNASSIGNED — a gap we are declaring. Distributed
ownership degrades a routing layer into an untrusted wiki page within two quarters.

**6. How often is it reconciled?**
Target 90 days, distrust banner at 120. Freshness is a displayed, tracked metric.
The reconciler is explicitly forbidden from refreshing the date without a real
review; making stale look fresh is the worst available failure of this system.

**7. What is your biggest unmitigated risk?**
Open item #1: we have not enumerated which Data Use Agreements, CRO MSAs and
clinical trial agreements carry non-transferability clauses reaching model
prompting. It is the direct analog of NIH's controlled-access genomic rule and
the cell most likely to be wrong.

**8. Second biggest?**
Use cases 23–28 have exactly one permitted platform and therefore no swap
alternate. The registry records `NONE AVAILABLE` rather than naming a blocked
platform to fill the field.

**9. How do you handle PHI?**
No commercial platform is routed for identifiable patient data. Enclave and
validated instance are conditional on Privacy Officer sign-off with a DPIA. The
router itself never receives data of any class.

**10. HIPAA de-identified data — you allow that on commercial platforms?**
Conditionally, with two named approvers, and the cell states plainly that HIPAA
de-identified is not GDPR anonymous. If EU or UK subjects are in scope the answer
likely changes, which is open item #5.

**11. Do the vendors train on our data?**
Enterprise terms exclude it. We have **not read the executed contracts** — open
item #2. Until then that is a vendor claim, not a verified control.

**12. What about the EU AI Act?**
A live classification question for counsel, flagged in the ruleset anchors with
`confidence: medium`. Clinical use cases 29 and 30 are the plausible Annex III
candidates. We do not assert a conclusion.

**13. How do you prevent shadow AI?**
By being faster than the alternative. Blocked verdicts return three concrete
routes rather than a refusal. We measure latency and coverage; we do not measure
blocks. An unrouted "no" is the request that becomes a personal-account workaround.

**14. How do you know adoption is real?**
We deliberately do **not** manage on adoption counts — they are easy to inflate.
Six input metrics: coverage, latency, SLA attainment, evidence ratio, freshness,
swap readiness.

**15. What if a model version changes?**
Reconciliation event plus re-benchmark trigger. Evidence tags expire on version
change. GxP paths trigger a requalification assessment.

**16. Can this tool be manipulated to approve something?**
`route-advisor` reads the ruleset and is instructed never to synthesise a rule,
infer from a neighbouring cell, or soften a block. Ruleset writes are restricted
to the named owner and every change is in the changelog with a reviewer.

**17. What data does the tool retain?**
Class, work type, jurisdiction, verdict, timestamp, clarifying rounds. Never
request text — request text in a research organisation is itself sensitive.

**18. Why not standardise on one vendor?**
Because model rankings move with version and licensed tier, both of which change
on the vendor's schedule rather than ours, so the decision carries an expiry date
we do not control. The durable assets are the re-benchmark cadence and the swap
protocol. (We are careful not to over-claim here: the anecdote about two
published comparisons inverting is logged UNVERIFIED in
`docs/CLAIMS-REGISTER.md`.)

**19. What would make you shut this down?**
Written in advance in `docs/OPERATING-CADENCE.md`: flat intake coverage while
usage grows; latency no better than email; evidence ratio static for two
quarters; chronically missed SLAs. Any two together is a stop-and-rescope signal.

**20. What is not ready?**
The list is in the changelog: unsigned matrix, unread contracts, no DPIA, unknown
enclave qualification, no deemed-export analysis, unverified tenant
classification, no jurisdiction axis, zero EVIDENCE tags. The germline class now
exists as of ruleset `2.0.0-draft`, but both of its conditional cells assume a
consent and Data Use Certification answer nobody has produced yet (open item 9),
and its tier placement is a judgement rather than a determination (open item 10).

---

## Inspection posture

**Lead with the register.** Open the conversation with the nine open items. It
reframes the audit from discovery to review, and it is the accurate description
of a draft system.

**Never claim measurement you do not have.** The single fastest way to lose an
auditor is one `ASSUMED` score presented as a benchmark result. The tags exist so
this cannot happen by accident.

**Separate the tool from the platforms.** Most inspection scope attaches to the
platforms and to the validated instance. The router is a lookup table with a
changelog.

**Bring the negative results.** Refusal-calibration false-refusal rates and failed
swap drills are the artifacts that demonstrate the harness is real. A program
that only reports favourable numbers is not running a harness.

## Pre-inspection checklist

- [ ] Ruleset reconciled within target; freshness banner accurate
- [ ] Changelog current, reviewer named on every verdict change
- [ ] Open items each have an owner and a due date
- [ ] Every `EVIDENCE` tag traces to a run ID with variance reported
- [ ] No expired evidence tags presented as current
- [ ] Swap drill records current for high-blast-radius workflows
- [ ] Approver SLA attainment reported, including misses
- [ ] Intake log contains no request text (spot-check)
- [ ] Task packs contain no regulated data (spot-check every pack)
- [ ] Cost figures labelled PLACEHOLDER unless contracted
