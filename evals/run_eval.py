#!/usr/bin/env python3
"""BioRouter evaluation harness. Zero dependencies, Python 3.9+.

  python3 evals/run_eval.py --pack evals/taskpacks/bioinformatics-code.json \
      --models claude-opus-5,gpt-5.6-sol --repeats 5 --provider dry

Design rules enforced here rather than left to discipline:
  * unscored items stay unscored. A skipped interpreter, an unfilled citation
    allowlist and a hedged answer are absences of measurement, never zeros.
  * the decision-relevant uncertainty is reported ACROSS ITEMS, with a
    bootstrap CI, because the pack is a sample of tasks. Repeat-to-repeat
    noise is reported separately and is not the number that gates a claim.
  * a gap that does not clear the CI is printed as INDISTINGUISHABLE.
  * promotion to EVIDENCE requires a real provider, n>=5 repeats, and enough
    SCORED items for the pack's stated risk tier.
  * model versions are recorded verbatim; the pack is hashed for reproducibility.

The model id strings above are ILLUSTRATIVE. Pass ids your provider actually
serves; the runner does not validate them and a wrong id fails at the API call.
"""
import argparse
import hashlib
import json
import os
import random
import statistics
import sys
import uuid
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import SCORERS, SCORER_VERSION  # noqa: E402

BOOTSTRAP_N = 2000
RANDOM_SEED = 20260829


# ---------------------------------------------------------------- providers

def provider_dry(model, prompt, **kw):
    """Deterministic synthetic response. Exercises the pipeline, measures nothing."""
    h = hashlib.sha256((model + prompt).encode()).hexdigest()
    return ("[DRY RUN - synthetic response, not a measurement]\n"
            "```python\nresult = 42\n```\nPMID: 00000000\ndigest %s" % h[:12])


def provider_anthropic(model, prompt, max_tokens=2048, **kw):
    import urllib.request
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("ANTHROPIC_API_KEY not set")
    body = json.dumps({"model": model, "max_tokens": max_tokens,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"content-type": "application/json", "x-api-key": key,
                 "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    return "".join(b.get("text", "") for b in d.get("content", []))


def provider_openai(model, prompt, max_tokens=2048, **kw):
    import urllib.request
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY not set")
    body = json.dumps({"model": model, "max_completion_tokens": max_tokens,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions", data=body,
        headers={"content-type": "application/json",
                 "authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]


def provider_local(model, prompt, max_tokens=2048, **kw):
    """OpenAI-compatible local/enclave endpoint. Set BIOROUTER_LOCAL_URL."""
    import urllib.request
    base = os.environ.get("BIOROUTER_LOCAL_URL")
    if not base:
        raise SystemExit("BIOROUTER_LOCAL_URL not set")
    body = json.dumps({"model": model, "max_tokens": max_tokens,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body,
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]


PROVIDERS = {"dry": provider_dry, "anthropic": provider_anthropic,
             "openai": provider_openai, "local": provider_local}


# --------------------------------------------------------------- statistics

def _weighted_mean(pairs):
    num = sum(v * w for v, w in pairs)
    den = sum(w for _, w in pairs)
    return num / den if den else 0.0


def bootstrap_ci(pairs, iters=BOOTSTRAP_N, alpha=0.05, seed=RANDOM_SEED):
    """Percentile bootstrap CI for the weighted mean, resampling ITEMS.

    The pack is a sample of tasks, so the item is the unit of resampling. This
    is the interval a routing decision has to clear. With 6-10 items it will be
    wide, and that width is the finding: it is what "n>=40 items for a medium
    risk promotion" is actually about.
    """
    if len(pairs) < 2:
        return None
    rng = random.Random(seed)
    means = []
    for _ in range(iters):
        sample = [pairs[rng.randrange(len(pairs))] for _ in range(len(pairs))]
        means.append(_weighted_mean(sample))
    means.sort()
    lo = means[int((alpha / 2) * iters)]
    hi = means[min(iters - 1, int((1 - alpha / 2) * iters))]
    return [round(lo, 4), round(hi, 4)]


def paired_gap(a_items, b_items, iters=BOOTSTRAP_N, seed=RANDOM_SEED):
    """Bootstrap the PAIRED per-item difference between two models.

    Paired on the item, because the same items are run in both arms and item
    difficulty is the dominant variance component. Returns the mean gap, its
    CI, and whether that CI excludes zero.
    """
    common = [k for k in a_items if k in b_items]
    if len(common) < 2:
        return None
    diffs = [(a_items[k]["mean"] - b_items[k]["mean"], a_items[k]["weight"])
             for k in common]
    rng = random.Random(seed)
    means = []
    for _ in range(iters):
        s = [diffs[rng.randrange(len(diffs))] for _ in range(len(diffs))]
        means.append(_weighted_mean(s))
    means.sort()
    lo, hi = means[int(0.025 * iters)], means[min(iters - 1, int(0.975 * iters))]
    return {"n_paired_items": len(common),
            "mean_gap": round(_weighted_mean(diffs), 4),
            "ci95": [round(lo, 4), round(hi, 4)],
            "excludes_zero": bool(lo > 0 or hi < 0)}


# ------------------------------------------------------------------- runner

def run_item(fn, model, item, system, allow_exec):
    prompt = item["prompt"]
    if system:
        prompt = system + "\n\n" + prompt
    try:
        resp = fn(model, prompt)
    except Exception as e:                      # noqa: BLE001
        return None, {"error": "%s: %s" % (type(e).__name__, e)}
    scorer = SCORERS.get(item.get("scorer", "contains_all"))
    if scorer is None:
        return None, {"error": "unknown scorer %s" % item.get("scorer")}
    return scorer(resp, item.get("expect", {}), allow_code_exec=allow_exec)


def _redact(detail):
    """Never write a dual-use completion into the result file.

    refusal() flags under-refusals and ambiguous dual-use probes with
    restricted_handling. The run records that it happened and where to route
    it, not what the model said.
    """
    if detail.get("restricted_handling"):
        d = dict(detail)
        resp = d.pop("response", None)
        if resp is not None:
            d["response_withheld_sha256"] = hashlib.sha256(
                resp.encode("utf-8", "replace")).hexdigest()[:16]
        d["response_note"] = ("withheld from the result file; route to the "
                              "biosafety officer under restricted handling")
        return d
    return detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--models", required=True,
                    help="comma-separated EXACT version ids your provider serves")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--provider", default="dry", choices=sorted(PROVIDERS))
    ap.add_argument("--scaffold", default="zero-shot",
                    help="zero-shot | agentic | retrieval. Recorded, and must be held constant across arms.")
    ap.add_argument("--allow-code-exec", action="store_true",
                    help="Execute model-generated code. Hardened runner, NOT a sandbox. "
                         "Use only in a container or throwaway VM.")
    ap.add_argument("--out", default="evals/results")
    a = ap.parse_args()

    if a.repeats < 5:
        print("WARNING: n<5. Repeat noise will be unreliable and the run is "
              "not promotable.", file=sys.stderr)

    raw = open(a.pack, "rb").read()
    pack = json.loads(raw.decode())
    pack_sha = hashlib.sha256(raw).hexdigest()[:16]
    fn = PROVIDERS[a.provider]
    models = [m.strip() for m in a.models.split(",") if m.strip()]
    run_id = uuid.uuid4().hex[:8]
    system = pack.get("system_prompt", "")
    min_items = pack.get("promotion_requirements", {}).get("min_scored_items", 40)

    results = {}
    for model in models:
        per_item, review_queue, unscored = {}, [], {}
        for item in pack["items"]:
            scores, reasons = [], []
            for _ in range(a.repeats):
                s, detail = run_item(fn, model, item, system, a.allow_code_exec)
                if s is None:
                    detail = _redact(detail)
                    if detail.get("needs_human_review"):
                        # Cap samples per item: a reviewer wants to see variation,
                        # not five copies of every response in the file.
                        seen = sum(1 for q in review_queue if q["item"] == item["id"])
                        if seen < 2:
                            review_queue.append({"item": item["id"], "detail": detail})
                        reasons.append("human_review")
                    elif detail.get("skipped"):
                        reasons.append("skipped: " + str(detail.get("reason", "")))
                    elif detail.get("needs_authoring"):
                        reasons.append("pack defect: " + str(detail.get("error")))
                        print("  ! %s / %s: pack defect: %s" % (model, item["id"],
                              detail.get("error")), file=sys.stderr)
                    else:
                        reasons.append("error: " + str(detail.get("error")))
                        print("  ! %s / %s: %s" % (model, item["id"],
                              detail.get("error")), file=sys.stderr)
                    continue
                scores.append(s)
            if scores:
                per_item[item["id"]] = {
                    "mean": round(statistics.mean(scores), 4),
                    "repeat_stdev": round(statistics.stdev(scores), 4) if len(scores) > 1 else 0.0,
                    "min": round(min(scores), 4), "max": round(max(scores), 4),
                    "n_repeats_scored": len(scores), "weight": item.get("weight", 1),
                    "dimension": item.get("dimension", "general"),
                }
            else:
                # An item nobody scored is reported as unscored. It is never a 0.
                unscored[item["id"]] = sorted(set(reasons)) or ["no result"]

        pairs = [(v["mean"], v["weight"]) for v in per_item.values()]
        overall = round(_weighted_mean(pairs), 4) if pairs else None
        ci = bootstrap_ci(pairs) if pairs else None
        repeat_noise = (round(statistics.mean([v["repeat_stdev"] for v in per_item.values()]), 4)
                        if per_item else None)
        item_sd = (round(statistics.pstdev([v["mean"] for v in per_item.values()]), 4)
                   if len(per_item) > 1 else None)

        dims = {}
        for v in per_item.values():
            dims.setdefault(v["dimension"], []).append(v["mean"])
        dims = {k: round(statistics.mean(x), 4) for k, x in dims.items()}

        results[model] = {
            "overall_weighted_mean": overall,
            "ci95_across_items": ci,
            "n_items_scored": len(per_item),
            "n_items_unscored": len(unscored),
            "across_item_stdev": item_sd,
            "repeat_noise_mean_stdev": repeat_noise,
            "dimensions": dims, "items": per_item,
            "unscored_items": unscored,
            "review_queue": review_queue,
        }
        print("%-24s mean %s  CI95 %s  scored %d/%d  across-item sd %s  repeat noise %s"
              % (model,
                 "n/a" if overall is None else "%.3f" % overall,
                 ci, len(per_item), len(pack["items"]), item_sd, repeat_noise))
        if dims:
            print("%-24s dims %s" % ("", dims))
        if unscored:
            print("%-24s UNSCORED (not zeros): %s" % ("", dict(unscored)))

    # pairwise comparison, paired on the item
    comparisons = {}
    for i, m1 in enumerate(models):
        for m2 in models[i + 1:]:
            g = paired_gap(results[m1]["items"], results[m2]["items"])
            if not g:
                continue
            key = "%s vs %s" % (m1, m2)
            g["verdict"] = ("DISTINGUISHABLE at this n" if g["excludes_zero"]
                            else "INDISTINGUISHABLE at this n")
            comparisons[key] = g
            print("\n%s: gap %+.3f  CI95 %s  -> %s"
                  % (key, g["mean_gap"], g["ci95"], g["verdict"]))

    scored_counts = [r["n_items_scored"] for r in results.values()]
    enough_items = bool(scored_counts) and min(scored_counts) >= min_items
    promotable = a.provider != "dry" and a.repeats >= 5 and enough_items
    blockers = []
    if a.provider == "dry":
        blockers.append("dry provider is a pipeline test, not a measurement")
    if a.repeats < 5:
        blockers.append("n<5 repeats")
    if not enough_items:
        blockers.append("fewer than %d scored items (min scored: %s); the CI above "
                        "shows why this matters" % (min_items, min(scored_counts) if scored_counts else 0))

    out = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "harness": {"scorer_version": SCORER_VERSION,
                    "python": sys.version.split()[0],
                    "bootstrap_iters": BOOTSTRAP_N, "seed": RANDOM_SEED},
        "pack": {"id": pack.get("id"), "version": pack.get("version"),
                 "file": os.path.basename(a.pack), "sha256_16": pack_sha,
                 "n_items": len(pack["items"]),
                 "measurement_limits": pack.get("measurement_limits")},
        "config": {"provider": a.provider, "repeats": a.repeats,
                   "scaffold": a.scaffold, "models_verbatim": models,
                   "code_exec_enabled": a.allow_code_exec},
        "promotable_to_EVIDENCE": promotable,
        "promotion_blockers": blockers,
        "promotion_note": ("Eligible for evidence-auditor review." if promotable else
                           "NOT promotable: " + "; ".join(blockers)),
        "interpretation_notes": [
            "Uncertainty that matters is ci95_across_items. repeat_noise is "
            "temperature noise and will be near zero with deterministic scorers; "
            "it is not evidence of precision.",
            "Unscored items are absences of measurement, not zeros. Read "
            "unscored_items before quoting any mean.",
            "Pairwise verdicts are uncorrected for multiple comparisons. With k "
            "models you are making k(k-1)/2 comparisons; treat a single "
            "DISTINGUISHABLE among many as a hypothesis, not a result.",
        ],
        "results": results,
        "comparisons": comparisons,
    }
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "%s-%s-%s.json" % (
        pack.get("id", "pack"), datetime.now().strftime("%Y%m%d"), run_id))
    json.dump(out, open(path, "w"), indent=2)
    print("\nrun %s -> %s" % (run_id, path))
    print(out["promotion_note"])


if __name__ == "__main__":
    main()
