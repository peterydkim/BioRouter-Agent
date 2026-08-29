---
description: Model total cost of ownership for a routed workflow from visible, editable assumptions. Refuses to price a blocked path.
argument-hint: [workflow and scale, e.g. "25 seats of agentic coding on de-identified data"]
---

Cost model for: **$ARGUMENTS**

1. Route it first via `route-advisor`. If the verdict is `blocked`, **stop**.
   Output the escalation and the three routes, and produce no number. Pricing a
   path nobody may use is how a governance tool becomes a liability.
2. Invoke `cost-modeler` with the routed platform.
3. Read every rate from `costmodel/assumptions.json`. Print the basis string next
   to each line. State on the output that no figure is a quote.
4. Where a rate is unknown, run low / expected / high rather than inventing a
   point estimate, and name which workflows become uneconomic at the high end.
5. Report **all-in per seat per year**. That is the number leadership can defend.

Include the lines people forget: support and enablement FTE, revalidation per
model version, exception handling per conditional gate, a continuity reserve for
any platform flagged `watch`, and the GxP premium where the path touches a
validated record. That last line routinely dwarfs licensing.
