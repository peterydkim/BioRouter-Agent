---
description: Answer an audit, inspection or due-diligence question from the repository's artifacts only, or run the pre-inspection checklist. Never improvises a control.
argument-hint: [the auditor's question, "pre-inspection", or "binder" for the full evidence map]
---

Audit question: **$ARGUMENTS** (pre-inspection checklist if empty).

Invoke `audit-liaison`. Read `docs/AUDIT-READINESS.md` — it holds the evidence
binder, the twenty questions with answers written to be given verbatim, and the
checklist.

**Lead with the open-items register.** Opening with the known gaps reframes the
audit from discovery to review, and it is the accurate description of a draft
system. An auditor should learn every weakness of this system from us, in
writing, before they find it.

Every answer points at an artifact: `rulesets/ruleset.v1.json`,
`rulesets/CHANGELOG.md`, `evals/results/`, `evals/taskpacks/`,
`registry/workflows.json`, `registry/intake-log.jsonl`,
`costmodel/assumptions.json`, `docs/`. Quote the cell, give its date and its
signature status, and state the basis tag — `ASSUMED` is said out loud as
"assumed, not tested."

**Where no artifact exists, say no control exists**, and give the open-item
number, its owner and its due date. Do not describe an intended control in the
present tense, do not generalise from a similar control that does exist, and do
not soften "nobody has signed this." An improvised control is worse than a gap:
a gap is a finding, an improvised control that turns out to be aspirational
contaminates every other answer given that day. If the gap is not on the
register, say so — that is a finding you just generated for yourself, which is
the correct outcome.

Bring the negative results: false-refusal rates, failed swap drills, missed
approver SLAs, expired evidence tags. A program that only reports favourable
numbers is not running a harness, and an experienced auditor knows it within two
questions.

Three answers that collapse scope and are true: the router is not a validated
system and does not need to be; it holds no personal data, only the tuple; and
accountability stays with the sponsor and never transfers to a vendor or a model.
