#!/usr/bin/env python3
"""Generate the static web app's data payload from the canonical ruleset.

    python3 tools/build_web.py

The web app must never carry its own copy of the matrix. A second copy is a
second source of truth, and the one on the website is the one people would
actually read. So `web/data/` is generated at build time, git-ignored, and
derived from `rulesets/ruleset.v1.json` on every deploy.

Everything the app displays is computed here, so the browser does no policy
reasoning: it renders what the ruleset already says.
"""
import json
import os
import collections
import hashlib
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "rulesets", "ruleset.v1.json")
OUT_DIR = os.path.join(ROOT, "web", "data")


def main():
    raw = open(SRC, "rb").read()
    d = json.loads(raw.decode())

    verdicts = collections.Counter()
    for row in d["matrix"].values():
        for cell in row.values():
            verdicts[cell["verdict"]] += 1

    basis = collections.Counter()
    for row in d["fit"].values():
        for f in row.values():
            basis[f["basis"]] += 1

    # Claim C1 in docs/CLAIMS-REGISTER.md is UNVERIFIED and is a commercially
    # consequential statement about a named vendor. The register's own
    # instruction is not to repeat it outside the company, and a public website
    # is as outside as it gets. The public payload therefore carries the
    # continuity LEVEL and the neutral doctrine, not the narrative.
    public_continuity = {"_doctrine": (
        "Availability is a contract variable, not a given. Any workflow that would be "
        "an emergency to move needs a written alternate before it goes to production. "
        "The specific incidents behind this doctrine are logged as UNVERIFIED claims "
        "in the project's claims register and are deliberately not restated here.")}
    for pid, flag in d["continuity_flags"].items():
        if pid.startswith("_"):
            continue
        public_continuity[pid] = {
            "level": flag.get("level"),
            "text": ("Carries a continuity watch. The underlying availability claim is "
                     "UNVERIFIED in this project's claims register, so it is not restated "
                     "on a public page; treat it as a reason to keep a verified alternate, "
                     "not as a finding about this vendor."
                     if flag.get("level") == "watch" else
                     "Model-version deprecation cadence is the live continuity risk rather "
                     "than withdrawal." if flag.get("level") == "normal" else
                     "You control availability for this platform."),
            "public_redacted": flag.get("level") == "watch"
        }

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256_16": hashlib.sha256(raw).hexdigest()[:16],
        "ruleset_version": d["ruleset_version"],
        "last_reconciled": d["last_reconciled"],
        "reconciliation_status": d["reconciliation_status"],
        "freshness_target_days": d["freshness_target_days"],
        "stale_after_days": d["stale_after_days"],
        "owner": d["owner"],
        "verdict_codes": d["verdict_codes"],
        "classification_scope": d.get("classification_scope", {}),
        "platforms": d["platforms"],
        "data_classes": d["data_classes"],
        "approver_roles": d["approver_roles"],
        "use_cases": d["use_cases"],
        "matrix": d["matrix"],
        "fit": d["fit"],
        "continuity_flags": public_continuity,
        "regulatory_anchors": d["regulatory_anchors"],
        "stats": {
            "cells": sum(len(r) for r in d["matrix"].values()),
            "platforms": len(d["platforms"]),
            "data_classes": len(d["data_classes"]),
            "permitted": verdicts[2],
            "conditional": verdicts[1],
            "blocked": verdicts[0],
            "basis": dict(basis),
        },
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "ruleset.json")
    with open(path, "w") as f:
        json.dump(payload, f, separators=(",", ":"))

    print("wrote %s (%d cells, %d classes, ruleset %s, source %s)"
          % (os.path.relpath(path, ROOT), payload["stats"]["cells"],
             payload["stats"]["data_classes"], payload["ruleset_version"],
             payload["source_sha256_16"]))
    print("verdicts: %d permitted, %d conditional, %d blocked"
          % (verdicts[2], verdicts[1], verdicts[0]))
    print("fit basis: %s" % dict(basis))


if __name__ == "__main__":
    main()
