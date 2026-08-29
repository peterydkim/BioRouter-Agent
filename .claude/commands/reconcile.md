---
description: Walk the ruleset against current regulatory and contractual sources, produce a diff, update the freshness stamp, and maintain the open-items register.
argument-hint: [optional: a specific class, platform, or regulation to focus on]
---

Reconcile the ruleset. Focus: **$ARGUMENTS** (whole matrix if empty).

Invoke `ruleset-reconciler`.

Priority order for sources — **company-internal contracts first**, because most
cells in this matrix are ultimately set by an agreement rather than a regulation:
Data Use Agreements, CRO master service agreements, clinical trial agreements,
partner and consortium terms, current vendor enterprise contracts, and the
validation status of the GxP instance. Then regulators, then privacy and export
rules, then vendor published terms.

Output the four counts: CHANGED, CONFIRMED, UNVERIFIABLE, OPEN ITEMS.

Two rules that are not negotiable:
- **Never refresh `last_reconciled` without an actual review.** Making a stale
  ruleset look fresh is the worst available failure of this system.
- **Cells you cannot verify go on the open-items register with an owner and a due
  date.** They do not get a guess. An honest "unverifiable" is the artifact that
  gets you the meeting with the person who can answer it.

Append to `rulesets/CHANGELOG.md` with the reviewer named and the signature
status stated. Bump the semantic version.
