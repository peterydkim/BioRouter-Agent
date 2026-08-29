---
description: Route a piece of work to a permitted platform. Returns the platform, the rule, the approver, the fit score with its basis tag, and the ranked alternatives.
argument-hint: [describe the work and the data class, e.g. "RNA-seq code on de-identified trial samples"]
---

Route this request: **$ARGUMENTS**

1. Invoke `intake-triage` to convert the request into a structured tuple. If the
   user pasted any actual data, stop and tell them to remove it — you need the
   classification, never the content.
2. Invoke `route-advisor` with the tuple.
3. If the verdict is `permitted` or `conditional` and the user asked about cost,
   invoke `cost-modeler`. If the verdict is `blocked`, **do not** produce a cost
   figure under any circumstance.
4. If the work is headed for production, invoke `swap-warden` to check whether a
   verified alternate is registered.

Lead with the ruleset freshness banner and the signature status. Every fit score
carries its basis tag, and `ASSUMED` is stated as "assumed, not tested."
