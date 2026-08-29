# From the NIH Router to a biotech/pharma estate

What carried over unchanged, what had to be rebuilt, and what is new.

Source: *NIH GenAI Router*, PR/FAQ and case study, Peter Kim, August 2026.

---

## Carried over unchanged — the transferable part

These are the design decisions that had nothing to do with being a federal agency.

| Idea | Why it transfers |
|---|---|
| Permission scored separately from capability | Allowed and good-at-it are different questions in any regulated industry |
| Basis tags on every capability score | Assumption-as-measurement is a universal failure mode |
| Refuse to price an unauthorized path | A governance tool that prices the forbidden becomes a liability anywhere |
| The tool never receives the data, only its classification | Same logic, stronger in pharma where trade secret joins privacy |
| Every conditional resolves to a named role and an SLA | Inboxes produce shadow AI in any organization |
| Versioned ruleset with a displayed freshness date and one owner | Distributed ownership degrades to an untrusted wiki page in two quarters |
| Do not standardize on one vendor; own the cadence and the swap | Published rankings invert inside twelve months regardless of sector |
| Manage on input metrics, not adoption counts | Adoption targets produce adoption theatre everywhere |

## Rebuilt — same shape, different content

| NIH | Industry | What changed |
|---|---|---|
| CHIRP, the widest sanctioned envelope | **Private research enclave** | The role is identical: the destination for what commercial platforms cannot hold. In industry you build or rent it rather than inheriting it. |
| ChatGPT Enterprise / Gemini / Claude via HHS | The same three under **commercial enterprise agreements** | The constraint moves from a government authorization to a *contract*. Retention windows, training exclusions and subprocessor lists become the reconciliation surface. |
| M365 Copilot in the tenant | Unchanged | Tenant-grounded productivity, different owner than the scientific platforms, and the guidance is the same: do not move research data into the tenant to reach it. |
| **NOT-OD-25-081** — controlled-access genomic data may not go to a public AI tool through prompts; the bar is the Data Use Certification, not identifiability | **Non-transferability clauses in DUAs, CRO MSAs and clinical trial agreements** | *The single most important mapping in this document.* The structure is identical: a **contractual** restriction that de-identification does not cure and a vendor security certification does not satisfy. In industry it is more dangerous because it is fragmented across many agreements rather than published in one notice. |
| dbGaP controlled-access class | `clin-deid` and partner-sourced data | Same trap, harder to see. Nobody publishes your DUA portfolio. Legal must enumerate it. |
| FedRAMP authorization | SOC 2, ISO 27001, contractual terms | Neither cures a contractual transfer restriction. That is the point both versions make. |
| IC Information System Security Officer | ISSO, DPO, QA CSV lead, Empowered Official, QPPV | The approver set fragments. More roles, shorter SLAs needed, same principle: name a role, never an inbox. |
| GSA OneGov rate expiry | Enterprise agreement renewal | Same posture: when a rate lapses without a published successor, model a range and never carry the lapsed rate forward. |

## New — no NIH equivalent

**1. The validated GxP instance.** The single largest addition. Nothing in the
NIH version corresponds to an environment under 21 CFR Part 11 with audit trail,
attributability and change control. It creates:
- a data class (`gxp-record`) with exactly one permitted platform
- a cost line (qualification and requalification) that routinely dwarfs licensing
- a version-lag capability penalty that is a *feature*, not a defect
- a swap category where the alternate is honestly `NONE AVAILABLE`

**2. Model risk as a formal construct.** The FDA credibility-assessment framework
gives industry something NIH's version had to improvise: a defensible way to
decide *how much evidence a claim needs*, derived from model influence and
decision consequence. This became `.claude/skills/credibility-assessment/`, and it
is now the spine of the evaluation harness.

**3. Export control and dual-use biology as a routing class.** Enclave
containment does not resolve the deemed-export rule; a foreign national accessing
your own enclave can still be an export.

**4. Pharmacovigilance.** Safety case data carries a *reporting obligation*, not
just a confidentiality one. No NIH analog.

**5. Refusal calibration as a first-class capability metric.** Present in the NIH
research as a researcher complaint; promoted here to a measured pack with a
false-refusal and under-refusal pair. In a pharma setting a model that refuses a
valid toxicology question is broken for the use case.

## Deliberately not carried over

- **Specific NIH institute names and presets.** Replaced with a generic estate.
- **The GSA OneGov pricing figures.** Federal-specific, and lapsed.
- **The claim that four platforms already exist and are free to the user.** In
  industry somebody pays, and the cost model is correspondingly load-bearing
  rather than illustrative.
- **The specific fit scores.** They were `ASSUMED` in the original and remain
  `ASSUMED` here. Nothing was laundered into `EVIDENCE` by being copied across.

## What is still unverified, stated plainly

Every cell in `rulesets/ruleset.v1.json` is a starting hypothesis derived from
public regulatory text. `reconciliation_status` reads UNSIGNED. No security,
privacy, QA or legal reviewer has walked the matrix, and the cells most likely to
be wrong are exactly the ones this file cannot see — your contracts. That is not
a defect in the design; it is the first ninety days of the job.
