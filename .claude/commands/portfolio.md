---
description: Place, sequence or review AI use cases across the R&D value chain. Derives model risk from influence and consequence, and orders adoption by evidence-bar reachability rather than by value.
argument-hint: [a use case to onboard, a wave to review, or empty for the whole portfolio]
---

Portfolio: **$ARGUMENTS** (full portfolio review if empty).

Invoke `portfolio-strategist`. Read `docs/USE-CASE-PORTFOLIO.md` first — it holds
the thirty placed use cases and the four findings, and you are maintaining it
rather than re-deriving it from memory.

**Onboarding a new use case** runs workflow W3 in this order:

1. `portfolio-strategist` — place it on the value chain and derive model risk
   from **model influence × decision consequence**. Do not tier by subject
   matter. Load `.claude/skills/credibility-assessment/SKILL.md` for the
   influence and consequence definitions and the evidence-bar table.
2. `intake-triage` — the data class, **including destination**. Output landing in
   a submission module is `gxp-record` however innocuous the inputs are.
3. `route-advisor` — permitted platforms at that class, read from the ruleset.
   Never write "probably permitted."
4. Evidence-gap check against `evals/taskpacks/`. If no pack covers the context
   of use, that pack is a prerequisite for production, not a follow-up.
5. `privacy-guardian` — DPIA trigger check if any personal data is in scope.
6. `cost-modeler` — only if a permitted path exists.
7. `swap-warden` — register with a verified alternate before production.

**Gate:** no production entry without (a) a permitted path, (b) an evidence
position stated with its basis tag, and (c) a registered alternate or an explicit
`NONE AVAILABLE` with a named risk owner.

**Reviewing waves.** Sequence by evidence-bar reachability, not by value. Wave 1
is not the easy stuff — it is how you build the evidence machine, the intake
habit and the approver relationships that make Wave 3 possible. A program that
starts at CSR drafting never gets to CSR drafting.

Three things this command does not produce: a quantified benefit figure (value
estimates are judgement and are labelled as such), an enterprise-wide winner, and
a fit score without its basis tag. If the portfolio still carries zero `EVIDENCE`
tags, lead with that number.
