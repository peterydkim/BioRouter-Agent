# BioRouter

**A governed routing and evaluation layer for the generative-AI platforms a
biotech or pharmaceutical company already licenses.**

> ## ⚠️ This is a design sketch. It is not a tested or validated system.
>
> Nobody has reviewed any of it. **Do not use it to make a real routing,
> compliance, procurement, or regulatory decision.**
>
> - **No reviewer has signed the permission matrix** — not security, not privacy,
>   not QA, not legal, not an export-control officer. All 78 verdicts are
>   hypotheses derived from public regulatory text.
> - **No capability score has ever been measured.** All 60 are inference from
>   vendor documentation, tagged `ASSUMED`.
> - **No task pack has been run against a real model.** Every run to date used
>   the synthetic dry provider, which measures nothing by construction.
> - **No cost figure is a quote.** Every rate is a placeholder.
> - **No workflow is a real registration**, and no ruleset owner is named.
> - **Seven of this project's own ten doctrinal claims are UNVERIFIED**, tagged
>   in `docs/CLAIMS-REGISTER.md`.
>
> The *code* is tested — 36 scorer regression tests, a repository validator, and
> CI on every push. That is not the same thing as the *content* being right, and
> it is important not to confuse the two. Passing tests here means the harness
> does what it claims; it says nothing about whether any verdict in the matrix is
> correct for your company.
>
> Treat it as a worked argument about how such a system should be structured,
> and as a starting point for reconciliation with your own counsel, security and
> QA. Not as an answer.

Your scientists have four or five sanctioned AI platforms. Each carries a
different data ceiling, and the differences are not intuitive. The platform
cleared for de-identified trial data is not the one cleared for BD material,
none may hold identifiable PHI, and partner-sourced data is governed by a
contract rather than by identifiability. A scientist with a novel study design
reads four policy pages, guesses, or emails three offices and waits a week.

BioRouter answers one question for that scientist, in under a minute:

> For this piece of work, on this data, which platform am I permitted to use,
> how good is it actually at this, what does it cost, and who signs when the
> answer is conditional?

The quiet failure mode in enterprise AI is not misuse. It is scientists pasting
work into whichever tool answers fastest, or abandoning the tool entirely.

Adapted from the *NIH GenAI Router* case study (Peter Kim, August 2026), which
argued that the scarce asset in an enterprise AI program is not model access but
**a maintained answer with an owner**.

> Nobody needs a fifth model. They need to know which of the four they already have.

---

## Who this is for

- **AI / Data Science leadership** at pharma and biotech standing up governed
  access to ChatGPT Enterprise, Claude Enterprise, Gemini, and Copilot
- **QA / Compliance / Legal** who need permission and capability tracked as
  separate, auditable artifacts
- **Platform teams** who are tired of the "fifth model" conversation and want a
  maintained answer with an owner

## What the system does

| Command | Does |
|---|---|
| `/route` | Permitted platform + the governing rule + residual risk + named approver + ranked alternatives, in under a minute |
| `/evaluate` | Designs and runs domain task packs; converts `ASSUMED` fit scores to `EVIDENCE` |
| `/reconcile` | Walks the ruleset against current regulation and contracts; maintains freshness and the open-items register |
| `/cost` | TCO from visible, editable assumptions. Refuses to price a blocked path |
| `/swap-drill` | Keeps every production workflow's alternate platform verified, drilled, and costed |
| `/scorecard` | Six managed input metrics; lagging outputs reported, not targeted |
| `/portfolio` | Places and sequences use cases across the R&D value chain by evidence-bar reachability |
| `/audit` | Answers an inspection question from artifacts only, or runs the pre-inspection checklist |
| `/dpia` | DPIA trigger check; tests the de-identification, consent-scope and transfer claims |

## The ten agents

```
                      /route
                         |
                  intake-triage ──── converts free text to a tuple.
                         |            Never accepts the data itself.
                         |
                  privacy-guardian ── DPIA trigger, de-identification
                         |             claims, transfers. Screens; never
                         |             grants a lawful basis.
                  route-advisor ───── the decision. Reads the ruleset,
                    /       \         never invents a rule.
                   /         \
          cost-modeler    swap-warden
        (refuses blocked)  (verified alternate before production)

                      /evaluate
                         |
                   eval-harness ───── runs domain packs
                         |
                 evidence-auditor ─── seven adversarial attacks.
                         |            May downgrade anything.
              ruleset-reconciler ──── versions, stamps freshness.
                                      Proposes; the owner applies.

                      /portfolio                    /audit
                         |                             |
              portfolio-strategist              audit-liaison
        (influence × consequence, never      (answers from artifacts only.
         by subject matter)                   Never improvises a control.)
```

## The four skills

| Skill | Loaded by |
|---|---|
| `credibility-assessment` | Anything that has to decide how much evidence a claim needs |
| `taskpack-authoring` | `eval-harness`, when a pack is written or sent back |
| `data-classification` | `intake-triage` and `privacy-guardian`, before any class is committed |
| `refusal-calibration` | `eval-harness`, before refusal items are authored or interpreted |

## What's in here

| Path | What it is |
|---|---|
| `rulesets/ruleset.v1.json` | The permission matrix: platforms × data classes, with the rule cite and approver for every cell. **The core maintained asset.** |
| `rulesets/CHANGELOG.md` | Version history, reconciliation dates, and the open-items register |
| `evals/` | Task packs, the zero-dependency harness, the scorers, and the scoring rubric |
| `registry/` | Production workflows with verified alternates; the intake log |
| `costmodel/assumptions.json` | Every rate, visible and editable. No figure here is a quote |
| `docs/` | Design principles, data governance, audit readiness, use-case portfolio, claims register |
| `tools/` | The invariants that are controls rather than norms. Run in CI |
| `.claude/` | Agent, skill and command definitions |

## Getting started

```bash
git clone https://github.com/peterydkim/BioRouter-Agent.git
cd BioRouter-Agent
claude
```

Then:

```
/route RNA-seq analysis code on de-identified trial samples from a CRO
```

Validate the harness pipeline without API keys or spend:

```bash
python3 evals/run_eval.py --pack evals/taskpacks/variant-calling.json --models model-a,model-b --repeats 5 --provider dry
```

The dry provider returns a fixed synthetic string, so its scores are meaningless
by construction — it exists to prove the pipeline runs. Expect near-zero means, a
wide confidence interval, and `INDISTINGUISHABLE at this n`. On
`refusal-calibration` expect **every item unscored**: a synthetic string is
neither a refusal nor a substantive answer, and the scorer refuses to guess
rather than invent a rate.

A real run needs `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` and `--provider anthropic`
or `openai`. Model ids in these examples are **illustrative** — pass ids your
provider actually serves. Zero dependencies, Python 3.9+.

Code-executing items are off unless you pass `--allow-code-exec`, and that flag
runs model-generated code. It is a hardened runner, not a sandbox: use it in a
container, never on a machine holding regulated data.

## The web app

**Live: [biorouter-agent.netlify.app](https://biorouter-agent.netlify.app)**

A static routing interface over the same ruleset lives in `web/`. It has no
server, no backend and no storage, which is not a cost saving — it is rule 4
made structural. **A page with no backend cannot receive the data it governs.**
Users pick a work type, a data class, a destination and optionally a platform;
everything is evaluated in the browser.

```bash
python3 tools/build_web.py   # derives web/data/ruleset.json from the ruleset
```

`web/data/` is generated and git-ignored. The app carries no copy of the
permission matrix, because a second copy becomes a second source of truth and
the one on the website is the one people would actually read. CI regenerates it
and fails if it does not match the canonical matrix.

The app is deliberately missing one thing: **there are no cost figures in it at
all.** Every rate in the repository is a placeholder, and a blocked verdict
returns three routes and no number.

## Checks

```bash
python3 tools/validate.py && python3 tools/test_scorers.py
```

Most of this repository's rules live in agent prose, which is a norm. These two
files are the part that is a **control**, and they run in CI on every push:

| Check | Fails the build when |
|---|---|
| `validate.py` — ruleset | a cell is missing, a conditional names no approver, an `EXTERNAL` tag has no citation, an `EVIDENCE` tag has no run file |
| `validate.py` — packs | a token is a stopword or a bare single-letter flag, a hard negative uses a scorer that would punish the correct answer, a citation item has an empty allowlist, a prompt looks like it contains regulated data |
| `validate.py` — registry | a registered alternate is *blocked* for its workflow's data class, or the intake log contains request text |
| `validate.py` — docs | a count quoted in prose disagrees with the ruleset |
| `test_scorers.py` | any of the 36 pinned scorer behaviours regresses |

## The six task packs

| Pack | Why it exists |
|---|---|
| `bioinformatics-code` | **R and Nextflow** are under-represented in public coding benchmarks relative to Python, and that gap is where scientist frustration concentrates |
| `literature-grounding` | "No hallucinations" is a marketing claim until it is a measured rate. Includes a fabricated-paper probe |
| `regulatory-writing` | High consequence, near-zero public benchmark coverage. Includes a no-data compound where any specific number is invented |
| `omics-interpretation` | Isolates domain *reasoning* from tool *orchestration*. Includes a perfectly confounded experiment where the correct answer is "no conclusion available" |
| `refusal-calibration` | A model that refuses a valid toxicology question is broken for the use case. No vendor publishes this number |
| `variant-calling` | Single-gene targeted sequencing, where almost every failure is **silent** — the pipeline runs and the VCF is wrong |

The shipped packs are 5–10 item templates showing the shape. A pack supporting a
real `EVIDENCE` promotion needs **40+ scored items for medium risk, 60+ for
high**, authored with a domain reviewer — each pack declares its own bar in
`promotion_requirements`, and the runner refuses to mark a run promotable below
it. Every shipped pack is currently below its own bar, which is why no cell
carries an `EVIDENCE` tag.

## Current honest state

| | |
|---|---|
| Ruleset | `2.1.0-draft`. 78 cells, 6 platforms × 13 data classes. **UNSIGNED** — no security, privacy, QA or legal review has occurred |
| Verdicts | 37 permitted · 20 conditional · 21 blocked |
| Fit basis | **60 ASSUMED · 0 EXTERNAL · 0 EVIDENCE**. Five cells were tagged `EXTERNAL` on an uncited literature and were downgraded on 2026-08-29 |
| Cost rates | Every figure is a PLACEHOLDER. None is a quote |
| Workflows | Two worked examples, no real registrations |
| Open items | 9 logged in `rulesets/CHANGELOG.md`. #8 closed by the germline class; #9 and #10 opened in its place |
| Own claims | 10 in `docs/CLAIMS-REGISTER.md`, **7 UNVERIFIED**. Tagged rather than quietly asserted |
| Evidence runs | None. `evals/results/` is empty and no cell cites a run |
| Checks | `tools/validate.py` + `tools/test_scorers.py`, run in CI on every push |

That fit distribution is what an honest day-one table looks like, and it got
worse on review rather than better: five cells that read `EXTERNAL` were pointing
at a literature they never cited, so they were downgraded. Moving this ratio is
the entire purpose of the evaluation harness. Any version of this that shipped
claiming measured scores on day one would be the exact failure the design exists
to prevent.

**What the harness does not measure**, stated here because a pack score is easy
to over-read: no pack executes a bioinformatics pipeline, so `variant-calling`
scores prose about calling rather than a VCF; Nextflow items are keyword probes
because there is no Nextflow runner; and two `literature-grounding` items are
unscored until a human fills their citation allowlist. Each pack carries its own
`measurement_limits`, and the runner prints them into every result file.

## Before using this on real work

1. **Have Legal enumerate your Data Use Agreements** (open item 1). This is the
   direct analog of the NIH controlled-access rule and the cell most likely to be
   wrong in your estate.
2. **Have Security and Privacy walk the matrix** line by line until someone signs
   for one business unit.
3. **Replace every cost placeholder** with a contracted figure.
4. **Add a jurisdiction axis** if EU or UK subjects are in scope (open item 5).
5. **Answer the germline consent question** (open item 9). The `germline-seq`
   class has no self-service route on any platform by design, and both of its
   conditional cells currently assume a consent and Data Use Certification answer
   that nobody has produced.
6. **Run one real pack** and convert at least one cell to `EVIDENCE`.

---

## The seven rules (abridged)

1. **Permission and capability are different questions** and never merge into one score.
2. **Every capability score carries a basis tag** — `EVIDENCE`, `EXTERNAL`, or `ASSUMED`. Never present an assumption without the tag.
3. **Never price a path nobody may use.** A blocked verdict returns an escalation, not a number.
4. **The router never receives the data. Only its classification.**
5. **Every conditional path resolves to a named role and an SLA, never an inbox.**
6. **The ruleset is a versioned artifact** with a displayed freshness date and one named owner.
7. **Do not standardize on a single vendor.** The durable assets are the re-benchmark cadence and the swap protocol.

## What this system does not do

- It does not build, fine-tune, or host a model.
- It does not grant authority. It surfaces authorizations that already exist, or
  states that none does.
- It does not touch PHI, PII, trade secret, or export-controlled material.
- It does not produce clinical decision support, diagnostic output, or a
  regulatory conclusion. Work is routed and costed, never interpreted.
- It does not name an enterprise-wide winner. That is the question the evidence
  says to stop asking.

## Further reading

Read `docs/DESIGN-PRINCIPLES.md` before changing any agent,
`docs/CLAIMS-REGISTER.md` before repeating any factual claim from this
repository, and `docs/NIH-to-industry-mapping.md` for what carried over from the
federal version and what had to be rebuilt for a commercial estate.

**A note on this repository's own claims.** Seven of the ten doctrinal claims
behind these design decisions are tagged `UNVERIFIED` — including the vendor
availability narrative that sets a `watch` flag on a named company. They are
reported and believed, not sourced. The register says so on each one, and the
design arguments are written to stand without them. Do not carry an `UNVERIFIED`
row into a regulator conversation, an audit, or a vendor negotiation.

## License

MIT — see [LICENSE](LICENSE).

---

*Independent work product. Not affiliated with, authorized by, or endorsed by NIH,
HHS, Booz Allen Hamilton, or any model vendor. Regulatory citations are starting
points for reconciliation with counsel, not legal advice.*
