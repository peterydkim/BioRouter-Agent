---
name: credibility-assessment
description: Scope any model evaluation to a context of use and a model risk before designing it, following the FDA seven-step credibility assessment framework. Use when designing a task pack, deciding how much evidence a claim needs, or defending an evaluation to QA, Regulatory or an auditor.
---

# Credibility assessment

The central move, and the one most evaluation programs skip: **you do not
evaluate a model. You evaluate a model for a specific context of use.**

The same model can be credible for drafting an internal literature summary and
not credible for triaging a safety case. An evaluation that does not name its
context of use cannot be defended to QA, and produces a number nobody can act on.

## The seven steps

1. **Define the question of interest.** What decision does this influence?
   Not "is the model good at biology" but "can this model correctly flag which
   of these variants warrant manual curation?"
2. **Define the context of use.** Precisely what the model does, what it is
   given, what it returns, and critically **what a human does with the output
   afterwards.** Write it in one paragraph. If you cannot, the scope is wrong.
3. **Assess model risk**, from two factors:
   - **Model influence** — how much of the decision rests on the model output
     versus other evidence? Autonomous action is high. One input among five that
     a domain expert reconciles is low.
   - **Decision consequence** — what happens if it is wrong? Patient harm and
     regulatory misstatement are high. An internal slide is low.

   Risk is the combination. **High influence with low consequence, and low
   influence with high consequence, are both moderate risk and need different
   mitigations** — the first needs accuracy, the second needs traceability.
4. **Develop the credibility assessment plan.** What evidence, at what volume,
   for that risk level. Write the acceptance criteria **before** running
   anything. This is the step that prevents the pack from being authored around
   the result.
5. **Execute the plan.** Run it as written.
6. **Document the results**, including deviations from the plan. A deviation you
   disclose is a finding; a deviation you quietly absorb is a credibility problem
   that surfaces during an audit.
7. **Determine adequacy** for the context of use. Not "is it good" but "is it
   good enough for this specific job." Then state the boundary of that
   conclusion.

## Risk to evidence, working table

| Model risk | Minimum evidence bar |
|---|---|
| Low | n>=5, one pack, `ASSUMED` acceptable if disclosed with the tag |
| Medium | n>=5, domain pack, variance reported, evidence-auditor review |
| High | n>=10, held-out pack authored by a domain reviewer, ablation isolating the model from the scaffold, human review of a sample, documented acceptance criteria set in advance |
| High + regulatory destination | All of the above, plus QA involvement, version pinning under change control, and a revalidation trigger on model version change |

## Reduce the risk instead of raising the bar

Often the cheapest correct answer is to change the context of use rather than
prove credibility at a high bar. Insert a human review step, narrow the output to
a flag rather than a conclusion, or restrict the input class. A high-influence
context of use redesigned into a low-influence one needs far less evidence, and
is usually the better system regardless.

## Writing it down

Every task pack carries a `context_of_use` field stating the influence,
consequence and resulting risk. A pack without one is not runnable, because
nobody can say what its score would mean.
