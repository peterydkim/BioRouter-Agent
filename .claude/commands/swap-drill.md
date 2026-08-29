---
description: Verify, drill, or execute the alternate-platform path for production workflows. Turns a vendor swap from an incident into a procedure with a known cost.
argument-hint: [workflow id, "all", or "event: <platform> unavailable"]
---

Swap readiness: **$ARGUMENTS**

Invoke `swap-warden`.

**Drill mode.** For each workflow in scope, confirm the registered alternate is
still ruleset-permitted for the same data class **today** — read the cell, do not
assume symmetry, and do not trust a verification from six months ago. Run the
workflow's regression set on the alternate. Record what **degraded**, not only
whether it completed: prompt scaffolding, tool-calling behaviour and refusal
boundaries all differ between vendors, and that is where drills actually fail.

**Event mode.** Order affected workflows by blast radius. Confirm each alternate
is permitted today. Hand GxP-flagged workflows to QA first, because a swap on a
validated path is a revalidation event and has the longest lead time. Log actual
swap hours against the estimate and correct the estimates afterward.

Report **swap readiness**: the share of production workflows with a verified,
drilled alternate. This is a managed input metric. The measure of success is that
the alternate was already written down before anyone needed it.
