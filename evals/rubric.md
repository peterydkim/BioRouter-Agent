# Scoring rubric and promotion rules

## Basis tags — the whole point of the system

| Tag | Means | May be used when |
|---|---|---|
| `EVIDENCE` | A local harness run on a named pack | n>=5, spread reported, version pinned, scaffold documented, `evidence-auditor` returned PROMOTE |
| `EXTERNAL` | A published study | Cited, and accompanied by the statement that it was not run on this company's work |
| `ASSUMED` | An inference from vendor documentation | Always allowed, but must be rendered to users as **"assumed, not tested"** |

Never present a score without its tag. A fit table where everything reads
`ASSUMED` is honest and useful. A fit table where an assumption is dressed as a
measurement is neither, and it is the most common way an enterprise AI rollout
goes wrong.

## Variance, and which variance

There are two, and confusing them is how a harness produces confident nonsense.

- **Repeat noise** — the same item run n times. With deterministic scorers it is
  near zero, and a near-zero number here is **not** evidence of precision. It is
  reported as `repeat_noise_mean_stdev` and it gates nothing.
- **Across-item variation** — the real uncertainty, because the pack is a
  *sample of tasks* and the item is the unit of resampling. The runner reports
  `ci95_across_items`, a percentile bootstrap over items, and that is the
  interval a routing claim has to clear.

Rules:

- **Minimum n=5 repeats.** Below that the runner marks the run unpromotable.
- **Minimum scored items** per the pack's `promotion_requirements`: 40 for
  medium risk, 60 for high. The runner counts items that actually scored, not
  items that shipped.
- **A gap whose paired CI includes zero is not a gap.** The runner prints
  `INDISTINGUISHABLE at this n` and you either raise n or stop claiming a
  difference. With a six-item template pack, everything is indistinguishable,
  and that is the correct answer rather than a defect.
- **Comparisons are uncorrected for multiplicity.** With k models you are making
  k(k-1)/2 comparisons; one `DISTINGUISHABLE` among many is a hypothesis.
- Single-shot comparisons between frontier models are noise. Fine for
  smoke-testing a pack, worthless for a routing decision.

## Absences are not zeros

A skipped interpreter, a disabled `--allow-code-exec`, an unfilled citation
allowlist, a `rubric_judge` item and a hedged refusal response all come back
**unscored**. The runner records them in `unscored_items` with a reason and
never folds them into the mean as failures.

This matters more than it sounds. Scoring a missing R interpreter as 0.0 would
have manufactured the finding "this model is bad at R" out of a dependency that
was never installed. Read `unscored_items` before quoting any mean: a run where
half the pack went unscored is a half-run.

## Scaffold discipline

Report **zero-shot and agentic separately, always.** Zero-shot accuracy on real
biomedical analysis tasks is poor across all vendors; iterative agentic planning
raises it substantially. A number that blends the two describes neither
condition, and it is the number vendors prefer you quote.

Hold the scaffold constant across arms — same retrieval, same tools, same loop —
or you are benchmarking your harness. Where you cannot hold it constant, run the
**ablation**: same model with and without the scaffold. That delta is usually the
most decision-relevant number in the whole run, because it tells you whether you
are buying a model or an integration.

## Version pinning

Record the exact version string: `claude-opus-5`, not "Claude". **The licensed
tier moves the score as much as the vendor does.** This is the single most common
error in published comparisons — a study comparing a free tier of one product
against a paid tier of another is measuring procurement, not capability. (The
claim that two such studies twelve months apart inverted each other's rankings is
C3 in `docs/CLAIMS-REGISTER.md` and is **UNVERIFIED**.)

## Promotion path

```
run (n>=5, pinned, documented scaffold)
  -> evidence-auditor: seven attacks
     -> PROMOTE                     -> propose fit cell edit to EVIDENCE + run ID + date
     -> PROMOTE WITH NARROWED SCOPE -> promote the named subset only; rest stays ASSUMED
     -> HOLD                        -> fix the named methodology gap, re-run
     -> DOWNGRADE                   -> return to ASSUMED with a one-line reason
```

`eval-harness` **proposes** the ruleset edit. The ruleset owner **applies** it.
An agent that can silently edit its own evidence base is not an evidence base.

## Human review queue

`rubric_judge` items are never auto-scored. A model grading a model on domain
quality is itself an unvalidated measurement that inherits the judge's biases.
Those items go to `review_queue` in the result file for a human domain reviewer,
and **a cell scored only by judge items cannot be promoted.**

Beyond the queue, read a sample of raw outputs on every run — twenty is enough.
Automated scorers catch hard failures and miss soft ones: the answer that is
technically responsive, heavily hedged, and useless to the scientist.

## Expiry

An `EVIDENCE` tag expires when the model version changes, or after two quarters,
whichever comes first. On expiry it reverts to `ASSUMED` until re-run. An
evidence tag with no expiry becomes a stale claim wearing a measurement's
authority.

**Refusal-calibration evidence expires on version change only** — never on the
two-quarter clock alone. Refusal boundaries move between versions and the
resulting breakage is silent: no error, no alert, just a scientist who stops
using the tool.
