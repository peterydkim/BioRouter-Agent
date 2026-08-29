#!/usr/bin/env python3
"""Mechanical invariant checks for the BioRouter repository. Zero dependencies.

    python3 tools/validate.py            # check everything, exit 1 on failure
    python3 tools/validate.py --quiet    # errors only

Most of this repository's rules live in agent prose, which a model may or may
not follow. The rules that can be checked by a machine are checked here, and
this runs in CI. The distinction matters: prose is a norm, this file is a
control, and only one of them survives contact with a bad day.

Checks:
  ruleset   every platform x data class cell exists, verdicts are legal,
            every conditional names a real approver, EVIDENCE/EXTERNAL fit
            tags carry the provenance their own rubric demands
  packs     required fields, discriminating tokens, scorer/expect agreement,
            no obviously regulated data
  registry  workflow entries reference real platforms and classes; the intake
            log carries no free text
  docs      counts quoted in prose match the ruleset
"""
import argparse
import json
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULESET = os.path.join(ROOT, "rulesets", "ruleset.v1.json")

# Duplicated from evals/score.py deliberately: a pack must not become valid by
# editing the scorer's stopword list.
STOPWORD_TOKENS = {
    "not", "no", "the", "and", "or", "but", "however", "also", "may", "can",
    "is", "are", "was", "were", "be", "been", "it", "this", "that", "with",
    "for", "from", "you", "your", "we", "should", "would", "could", "will",
    "log", "work", "use", "used", "using", "then", "than", "all", "any",
}

# Patterns that suggest real regulated material leaked into a task pack.
REGULATED_HINTS = [
    (r"\b\d{3}-\d{2}-\d{4}\b", "US SSN-shaped string"),
    (r"\bMRN[:\s#]*\d{4,}\b", "medical record number"),
    (r"\b(?:NCT)\d{8}\b.*\bpatient\b", "trial id next to patient reference"),
    (r"\b[ACGT]{60,}\b", "long raw nucleotide sequence"),
    (r"\b\d{1,2}/\d{1,2}/(?:19|20)\d{2}\b.*\b(dob|date of birth)\b", "date of birth"),
]

errors, warnings = [], []


def err(where, msg):
    errors.append("%s: %s" % (where, msg))


def warn(where, msg):
    warnings.append("%s: %s" % (where, msg))


# ------------------------------------------------------------------ ruleset

def check_ruleset():
    d = json.load(open(RULESET))
    where = "rulesets/ruleset.v1.json"

    platforms = [p["id"] for p in d["platforms"]]
    classes = [c["id"] for c in d["data_classes"]]
    approvers = set(d["approver_roles"])
    legal_verdicts = {int(k) for k in d["verdict_codes"]}

    if len(set(platforms)) != len(platforms):
        err(where, "duplicate platform ids")
    if len(set(classes)) != len(classes):
        err(where, "duplicate data class ids")

    # every cell present, legal, and conditionals resolve to a named role
    for p in platforms:
        row = d["matrix"].get(p)
        if row is None:
            err(where, "matrix missing platform %r" % p)
            continue
        for c in classes:
            cell = row.get(c)
            if cell is None:
                err(where, "matrix missing cell %s x %s" % (p, c))
                continue
            if cell.get("verdict") not in legal_verdicts:
                err(where, "cell %s x %s has illegal verdict %r" % (p, c, cell.get("verdict")))
            if not cell.get("rule", "").strip():
                err(where, "cell %s x %s has no rule text" % (p, c))
            if cell.get("verdict") == 1 and cell.get("approver") not in approvers:
                err(where, "conditional cell %s x %s names no valid approver (rule 5)" % (p, c))
            if cell.get("verdict") != 1 and cell.get("approver"):
                warn(where, "cell %s x %s is not conditional but names an approver" % (p, c))
        for c in row:
            if c not in classes:
                err(where, "matrix platform %s has unknown class %r" % (p, c))

    for role, meta in d["approver_roles"].items():
        if not isinstance(meta.get("sla_days"), int):
            err(where, "approver %r has no integer sla_days (rule 5)" % role)

    # basis tags must carry the provenance evals/rubric.md requires of them
    use_cases = {u["id"] for u in d["use_cases"]}
    for uc, row in d["fit"].items():
        if uc not in use_cases:
            err(where, "fit has unknown use case %r" % uc)
        for p, f in row.items():
            if p not in platforms:
                err(where, "fit %s has unknown platform %r" % (uc, p))
            basis, note = f.get("basis"), f.get("note", "")
            if basis not in ("ASSUMED", "EXTERNAL", "EVIDENCE"):
                err(where, "fit %s/%s has unknown basis %r" % (uc, p, basis))
            if not isinstance(f.get("score"), int) or not 1 <= f["score"] <= 5:
                err(where, "fit %s/%s score must be 1-5" % (uc, p))
            if basis == "EXTERNAL" and not f.get("citation"):
                err(where, "fit %s/%s is EXTERNAL with no citation field. "
                           "rubric.md defines EXTERNAL as a CITED published study; "
                           "an uncited one is ASSUMED." % (uc, p))
            if basis == "EVIDENCE" and not (f.get("run_id") and f.get("run_date")):
                err(where, "fit %s/%s is EVIDENCE without run_id + run_date" % (uc, p))
            if basis == "EVIDENCE":
                hits = glob.glob(os.path.join(ROOT, "evals", "results",
                                              "*%s*.json" % f["run_id"]))
                if not hits:
                    err(where, "fit %s/%s cites run_id %s with no result file"
                        % (uc, p, f["run_id"]))

    for k in ("last_reconciled", "freshness_target_days", "stale_after_days",
              "reconciliation_status", "ruleset_version"):
        if k not in d:
            err(where, "missing required key %r" % k)
    if d.get("stale_after_days", 0) <= d.get("freshness_target_days", 0):
        err(where, "stale_after_days must exceed freshness_target_days")

    return d


# -------------------------------------------------------------------- packs

REQUIRED_PACK_FIELDS = ["id", "version", "context_of_use", "why_this_pack",
                        "data_policy", "dimensions", "items",
                        "measurement_limits", "promotion_requirements"]


def check_packs():
    for path in sorted(glob.glob(os.path.join(ROOT, "evals", "taskpacks", "*.json"))):
        where = os.path.relpath(path, ROOT)
        d = json.load(open(path))
        for f in REQUIRED_PACK_FIELDS:
            if not d.get(f):
                err(where, "missing required field %r" % f)
        ids = set()
        for it in d.get("items", []):
            iid = it.get("id", "?")
            if iid in ids:
                err(where, "duplicate item id %r" % iid)
            ids.add(iid)
            scorer = it.get("scorer", "contains_all")
            exp = it.get("expect", {})

            if not it.get("prompt", "").strip():
                err(where, "%s: empty prompt" % iid)
            for pat, label in REGULATED_HINTS:
                if re.search(pat, it.get("prompt", ""), re.I):
                    err(where, "%s: prompt looks like it contains %s. Packs carry "
                               "public, synthetic or cleared material only." % (iid, label))

            if scorer in ("contains_all", "contains_any", "must_not_contain"):
                toks = exp.get("tokens", [])
                if not toks:
                    err(where, "%s: %s with no tokens" % (iid, scorer))
                for t in toks:
                    if t.lower().startswith("re:"):
                        try:
                            re.compile(t[3:])
                        except re.error as e:
                            err(where, "%s: bad regex token %r (%s)" % (iid, t, e))
                        continue
                    if t.lower() in STOPWORD_TOKENS:
                        err(where, "%s: token %r is a stopword and matches almost any "
                                   "prose. It cannot discriminate." % (iid, t))
                    if len(t.strip()) < 3 and not t.startswith("-"):
                        err(where, "%s: token %r is too short to discriminate; use a "
                                   "longer token or an re: pattern" % (iid, t))
                    if re.fullmatch(r"-[a-zA-Z]", t.strip()):
                        err(where, "%s: single-letter flag token %r matches inside "
                                   "long flags such as --reference. Use an re: "
                                   "pattern with boundaries." % (iid, t))

            if scorer == "must_not_contain":
                for t in exp.get("tokens", []):
                    if re.search(r"^[-\w.:]+\(?\)?$", t.strip()) and not t.lower().startswith("re:"):
                        err(where, "%s: must_not_contain token %r looks like the NAME of "
                                   "an entity. A correct denial has to name it. Use "
                                   "denies_existence instead." % (iid, t))

            if scorer == "denies_existence" and not exp.get("entity"):
                err(where, "%s: denies_existence requires expect.entity" % iid)

            if scorer == "citation_check":
                if not exp.get("valid_ids") and not exp.get("allowlist_pending"):
                    err(where, "%s: citation_check with an empty valid_ids and no "
                               "allowlist_pending flag. Every real citation would "
                               "score as fabricated." % iid)

            if scorer == "refusal":
                if exp.get("want") not in ("answer", "refuse"):
                    err(where, "%s: refusal item needs expect.want of answer|refuse" % iid)
                if exp.get("want") == "answer" and not exp.get("answer_markers"):
                    err(where, "%s: refusal want=answer needs answer_markers, or a "
                               "hedge scores as a served request" % iid)

            if scorer == "code_exec" and exp.get("lang") not in ("python", "r"):
                err(where, "%s: code_exec lang must be python or r (shell removed)" % iid)

            if it.get("dimension") and d.get("dimensions") and \
                    it["dimension"] not in d["dimensions"]:
                err(where, "%s: dimension %r not declared in pack dimensions"
                    % (iid, it["dimension"]))

        mn = (d.get("promotion_requirements") or {}).get("min_scored_items")
        if mn and len(d.get("items", [])) < mn:
            warn(where, "pack ships %d items but declares min_scored_items %d; runs "
                        "cannot be promoted until it is expanded (this is expected "
                        "for a template pack)" % (len(d.get("items", [])), mn))


# ----------------------------------------------------------------- registry

def check_registry(ruleset):
    platforms = {p["id"] for p in ruleset["platforms"]} | {"NONE AVAILABLE"}
    classes = {c["id"] for c in ruleset["data_classes"]}
    use_cases = {u["id"] for u in ruleset["use_cases"]}

    path = os.path.join(ROOT, "registry", "workflows.json")
    where = "registry/workflows.json"
    d = json.load(open(path))
    for w in d.get("workflows", []):
        wid = w.get("id", "?")
        if w.get("primary_platform") not in platforms:
            err(where, "%s: unknown primary_platform %r" % (wid, w.get("primary_platform")))
        if w.get("alternate_platform") not in platforms:
            err(where, "%s: unknown alternate_platform %r" % (wid, w.get("alternate_platform")))
        if w.get("data_class") not in classes:
            err(where, "%s: unknown data_class %r" % (wid, w.get("data_class")))
        if w.get("work_type") not in use_cases:
            err(where, "%s: unknown work_type %r" % (wid, w.get("work_type")))
        alt = w.get("alternate_platform")
        if alt in platforms and alt != "NONE AVAILABLE":
            cell = ruleset["matrix"][alt].get(w.get("data_class"), {})
            if cell.get("verdict") == 0:
                err(where, "%s: alternate %s is BLOCKED for %s. An alternate that is "
                           "blocked for the workflow's data class is not an alternate."
                    % (wid, alt, w.get("data_class")))
        if w.get("gxp_impact") in ("direct", "supporting") and not w.get("revalidation_required"):
            err(where, "%s: gxp_impact %r requires revalidation_required true"
                % (wid, w.get("gxp_impact")))

    # intake log: the tuple, never the request text
    log = os.path.join(ROOT, "registry", "intake-log.jsonl")
    lwhere = "registry/intake-log.jsonl"
    if not os.path.exists(log):
        err(lwhere, "missing. /scorecard reads this for coverage and latency; "
                    "without it two of the six input metrics are unmeasurable.")
        return
    allowed = {"_schema", "_note", "received_at", "resolved_at", "latency_seconds",
               "date", "work_type", "data_class", "jurisdiction", "confidence",
               "verdict_received", "clarifying_rounds", "approver_required",
               "sla_days", "sla_met", "destination", "volume_seats"}
    banned = {"prompt", "request", "text", "content", "excerpt", "sample",
              "identifier", "patient", "sequence", "file_path", "notes"}
    for n, line in enumerate(open(log), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            err(lwhere, "line %d is not valid JSON (%s)" % (n, e))
            continue
        if "_schema" in rec:
            continue
        for k in rec:
            if k in banned:
                err(lwhere, "line %d has field %r. The log records the tuple and the "
                            "outcome, never request text (design principle 4)." % (n, k))
            elif k not in allowed:
                warn(lwhere, "line %d has undeclared field %r" % (n, k))
        if rec.get("data_class") and rec["data_class"] not in classes:
            err(lwhere, "line %d has unknown data_class %r" % (n, rec["data_class"]))


# --------------------------------------------------------------------- docs

def check_docs(ruleset):
    n_cells = sum(len(r) for r in ruleset["matrix"].values())
    n_classes = len(ruleset["data_classes"])
    dist = {0: 0, 1: 0, 2: 0}
    for row in ruleset["matrix"].values():
        for cell in row.values():
            dist[cell["verdict"]] += 1
    basis = {}
    for row in ruleset["fit"].values():
        for f in row.values():
            basis[f["basis"]] = basis.get(f["basis"], 0) + 1

    md = glob.glob(os.path.join(ROOT, "*.md")) + glob.glob(os.path.join(ROOT, "docs", "*.md")) \
        + glob.glob(os.path.join(ROOT, ".claude", "**", "*.md"), recursive=True) \
        + glob.glob(os.path.join(ROOT, "rulesets", "*.md")) \
        + glob.glob(os.path.join(ROOT, "evals", "*.md"))
    for path in md:
        where = os.path.relpath(path, ROOT)
        txt = open(path).read()
        if where == "rulesets/CHANGELOG.md":
            continue                      # historical entries quote past counts
        for m in re.finditer(r"\b(\d{2,3}) cells\b", txt):
            if int(m.group(1)) != n_cells:
                err(where, "says %s cells; ruleset has %d" % (m.group(1), n_cells))
        for m in re.finditer(r"\b(\d{1,2}) data classes\b", txt):
            if int(m.group(1)) != n_classes:
                err(where, "says %s data classes; ruleset has %d" % (m.group(1), n_classes))
        for m in re.finditer(r"(\d+) permitted [·|]* (\d+) conditional [·|]* (\d+) blocked", txt):
            got = tuple(int(x) for x in m.groups())
            if got != (dist[2], dist[1], dist[0]):
                err(where, "verdict counts %s do not match ruleset %s"
                    % (str(got), str((dist[2], dist[1], dist[0]))))
        for m in re.finditer(r"(\d+) ASSUMED [·,] (\d+) EXTERNAL [·,] (\d+) EVIDENCE", txt):
            got = tuple(int(x) for x in m.groups())
            want = (basis.get("ASSUMED", 0), basis.get("EXTERNAL", 0), basis.get("EVIDENCE", 0))
            if got != want:
                err(where, "fit basis counts %s do not match ruleset %s" % (str(got), str(want)))

    # agent/skill/command files referenced in prose must exist
    for path in md:
        where = os.path.relpath(path, ROOT)
        for m in re.finditer(r"`(\.claude/(?:agents|skills|commands)/[\w./-]+)`", open(path).read()):
            if not os.path.exists(os.path.join(ROOT, m.group(1))):
                err(where, "references %s which does not exist" % m.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    ruleset = check_ruleset()
    check_packs()
    check_registry(ruleset)
    check_docs(ruleset)

    if warnings and not a.quiet:
        print("WARNINGS (%d)" % len(warnings))
        for w in warnings:
            print("  ~ %s" % w)
    if errors:
        print("\nERRORS (%d)" % len(errors))
        for e in errors:
            print("  x %s" % e)
        print("\nFAIL")
        return 1
    if not a.quiet:
        print("\nOK - %d cells, %d classes, %d packs validated"
              % (sum(len(r) for r in ruleset["matrix"].values()),
                 len(ruleset["data_classes"]),
                 len(glob.glob(os.path.join(ROOT, "evals", "taskpacks", "*.json")))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
