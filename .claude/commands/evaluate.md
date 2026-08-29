---
description: Design or run a model evaluation on a domain task pack, then send the result to adversarial review before any fit score is promoted.
argument-hint: [pack name or capability question, e.g. "bioinformatics-code across our three platforms"]
---

Evaluate: **$ARGUMENTS**

1. Load `.claude/skills/credibility-assessment/SKILL.md`. Name the context of
   use, the model influence, the decision consequence, and the resulting model
   risk **before** designing anything. State the evidence bar that risk implies.
2. Invoke `eval-harness`. If a suitable pack exists in `evals/taskpacks/`, use
   it. If not, load `.claude/skills/taskpack-authoring/SKILL.md` and draft one —
   including hard-negative items, which are the discriminating ones.
3. Run with `--repeats 5` minimum and the scaffold held constant across arms.
   Pin exact model versions. `--provider dry` validates the pipeline and is never
   a measurement.
4. Invoke `evidence-auditor` on the result. It runs seven attacks and returns
   PROMOTE, PROMOTE WITH NARROWED SCOPE, HOLD, or DOWNGRADE.
5. Only on PROMOTE, propose the edit to the `fit` block in
   `rulesets/ruleset.v1.json` — changing the basis tag to `EVIDENCE` and adding
   the run ID and date. **Propose the edit; do not apply it.** The ruleset owner
   applies changes.

Report mean and spread, never a bare score. Report zero-shot and agentic
separately. A two-point gap with a five-point spread is not a finding.
