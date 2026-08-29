---
name: taskpack-authoring
description: Write evaluation task packs that survive adversarial review. Use when creating or revising a pack in evals/taskpacks, or when a pack has been sent back by evidence-auditor.
---

# Authoring a task pack

A pack is a JSON file that must survive `evidence-auditor`. Write it expecting
to be attacked, because it will be.

## Required fields

`id`, `version`, `context_of_use`, `why_this_pack`, `data_policy`, `dimensions`,
`items`. A pack missing `context_of_use` is not runnable. `why_this_pack` must
answer: what does this measure that a public leaderboard already measures for
free? If there is no answer, do not build the pack.

## Item anatomy

```json
{"id": "...", "dimension": "...", "weight": 3, "prompt": "...",
 "scorer": "contains_all", "expect": {...}, "note": "why this item discriminates"}
```

## The linter is not optional

`python3 tools/validate.py` fails the build on the pack defects that have
actually bitten this repository. Run it before you commit a pack:

- a token that is a stopword or under three characters — `not` matches inside
  "another", `ad` inside "read", `umi` inside "Illumina"
- a bare single-letter flag token — `-r` matches inside `--reference`
- `must_not_contain` whose token is the *name* of a non-existent entity, which
  scores a correct denial zero and a hallucination one
- `citation_check` with an empty `valid_ids` and no `allowlist_pending`
- a `refusal` item with `want: answer` and no `answer_markers`
- a prompt that pattern-matches regulated data
- a missing `measurement_limits` or `promotion_requirements`

Tokens are matched with word boundaries. Where you need a stem or an
alternation, write the token as `re:<pattern>` — `re:significan`,
`re:-L\b|--intervals\b`.

## Scorer selection, and the one that is a trap

| Situation | Scorer |
|---|---|
| Required concepts must appear | `contains_all` |
| Any of several acceptable answers | `contains_any` |
| Fabricated **narrative** must not appear ("the study found") | `must_not_contain` |
| The prompt names a **thing that does not exist** | `denies_existence` |
| Cited identifiers must be real | `citation_check` with a filled allowlist |
| Code must actually run | `code_exec` (python or r; needs `--allow-code-exec`) |
| Refusal boundary, both directions | `refusal` with `answer_markers` |
| Only a human can judge it | `rubric_judge` |

**The trap:** reaching for `must_not_contain` on a hard negative. If the correct
answer has to *name* the fake function or flag in order to deny it, that scorer
punishes the behaviour you are trying to measure. Use `denies_existence`.

## Declare what the pack does not measure

Every pack carries `measurement_limits`, and the runner copies it into every
result file. Write it honestly: if no item executes a pipeline, say the pack
scores prose about the work rather than the work. This is the field that stops a
keyword score being quoted as a correctness rate.

## Rules that matter

1. **Do not draw items from public benchmarks.** The models may have trained on
   them. Author fresh items from real work, and keep the pack out of any public
   repository.

2. **Write hard negatives, and weight them heavily.** The most discriminating
   items are ones where the correct answer is *"this cannot be determined"* or
   *"that does not exist"*:
   - a fabricated function name the model should deny (`r-api-fidelity`)
   - a fabricated paper the model should fail to find (`fabricated-probe`)
   - a perfectly confounded experiment with no available conclusion (`batch-confound`)
   - a compound with no data, where any specific number is invented (`no-fabrication`)

   Models that pattern-match to a satisfying narrative fail these, and that is
   exactly the behaviour that costs you money in production. A pack of only
   positive items rewards fluency and measures little.

3. **One dimension per item.** An item that tests R syntax and DESeq2 statistics
   together tells you nothing when it fails.

4. **Never put regulated data in a pack.** Pack files are read by agents, live in
   a repository, and get copied. Public, synthetic, or cleared material only. If
   an item genuinely needs real data to be representative, move it to an
   enclave-only pack and say so in `data_policy`.

5. **Set acceptance criteria before you run.** Write the passing threshold into
   the pack. A threshold chosen after seeing results is not a threshold.

6. **Prefer deterministic scorers.** `contains_all` is blunt but reproducible and
   explainable to an auditor. Use `rubric_judge` only where automation genuinely
   cannot reach, and accept that those items go to a human queue and cannot
   support a promotion on their own.

7. **Version the pack and never edit items in place.** Changing an item
   invalidates comparison with prior runs. Bump the version and note what changed.

## Size

The shipped packs are six-to-ten-item templates that demonstrate the shape. A
pack supporting a real `EVIDENCE` promotion needs 40+ items for medium risk and
more for high risk, authored with a domain reviewer.
