# Data governance, security tiers and privacy

The controls behind the routing verdicts. Written to be read by a Privacy
Officer, a QA auditor, and a security architect without translation.

**Status: UNSIGNED.** Derived from public regulatory text. Every control below
needs confirmation against your actual contracts, your tenant configuration and
your validation record before it is operational.

---

## Principle: the router never holds regulated data

The system stores: a data **class**, a work type, a jurisdiction, a verdict, an
approver, and a timestamp. It does not store request text, sample identifiers,
file paths to regulated material, or model outputs.

This is not a convenience. A governance tool that ingested what it governs would
inherit every restriction it exists to route around — it would need its own
validation, its own DPIA, its own BAA, and it would become the highest-value
target in the estate. `intake-triage` refuses pasted content and the intake log
records the tuple and outcome only.

**Audit consequence:** the router itself is out of scope for GxP validation and
for most privacy assessments, because it processes no personal data. Say this
early in any assessment; it collapses a large amount of scope.

---

## Data classification ladder

Thirteen classes, ordered by tier. The tier is not a sensitivity score — it is a
*routing* ladder, and provenance can outrank content.

| Tier | Class | Definition | The trap |
|---|---|---|---|
| 1 | `public` | Published, public domain | — |
| 2 | `internal` | Internal, non-confidential | — |
| 3 | `cci` | Confidential commercial: pipeline, forecast, contract | Retention, not access, is the usual gap |
| 4 | `predec` | Pre-decisional: BD, M&A, licensing, diligence | Legal hold obligations attach |
| 4 | `research-unpub` | Unpublished preclinical, no human subjects | "No human subjects" must be verified, not assumed |
| 5 | `ts-chem` | Trade secret: chemical matter, sequences, process | Contractual no-training ≠ no-risk for crown jewels |
| 5 | `clin-anon` | Clinical, anonymised/aggregate | True anonymisation is rarer than claimed |
| 6 | `clin-deid` | De-identified under HIPAA | **Not GDPR anonymous.** See below |
| 7 | `germline-seq` | Human sequence **in the prompt**: reads, genotypes, variant calls, incl. the normal arm of a tumour-normal pair | **Cannot be de-identified.** But it classifies the prompt, not the subject |
| 7 | `pv` | Pharmacovigilance ICSR | Reporting obligation, not just confidentiality |
| 7 | `gxp-record` | Record supporting submission or batch release | **Destination, not origin, sets this class** |
| 8 | `clin-id` | Identifiable patient data, PHI, GDPR Art. 9 | — |
| 8 | `export-durc` | Export-controlled or DURC/PEPP-scoped | Enclave containment does not cure deemed export |

### The classification errors that cause incidents

**1. "It's de-identified, so it's fine."** HIPAA §164.514 de-identification
(Safe Harbor or Expert Determination) makes data non-PHI under US law. It does
**not** make it anonymous under GDPR — pseudonymised data remains personal data
with a full controller obligation. The same file is simultaneously
"de-identified" in Boston and "special category personal data" in Basel.

**2. "The prompt contains nothing sensitive."** Class is set by **destination as
well as origin**. A prompt containing only public method text lands in
`gxp-record` if the answer is pasted into a submission module. Intake must ask
where the output goes.

**3. "It came from our CRO, so it's ours."** Provenance outranks identifiability.
Partner, consortium and CRO agreements carry non-transferability clauses that a
prompt to a third-party model can breach **regardless of identifiability or
vendor security posture**. This is the direct analog of NIH's controlled-access
genomic rule, and it is harder to see because it is fragmented across many
contracts rather than published in one notice.

### The fourth error: "we stripped the identifiers off the sequence"

Genomic sequence is **re-identifying in its own right** — a modest number of SNPs
identifies an individual, and it identifies relatives who never consented.
HIPAA's 18 Safe Harbor identifiers do not list sequence data, which is a
recognised gap in the rule rather than a permission; GDPR Art. 9 names genetic
data explicitly. So removing a name from a VCF does not lower its class.

`clin-deid` handled this badly, and the dedicated `germline-seq` class was added
in ruleset `2.0.0-draft` (2026-08-29) to close open item #8. Affects portfolio
use cases 10, 11, 22, 30 — the genomics spine.

**There is no self-service route to this class on any platform.** The enclave and
the validated instance are conditional on the Privacy Officer; all four
commercial platforms are blocked. That is deliberate: authorisation for germline
sequence attaches to the named investigator and the approved research use, not to
the infrastructure, which is the direct analog of NIH controlled-access genomic
data. Containment alone never produces a `permitted` verdict here.

**Three boundaries keep this from over-blocking**, and they are load-bearing —
a class this restrictive fails by pushing work onto personal accounts, not by
letting data out:

1. **It classifies the prompt, not the subject.** Pipeline configuration,
   parameter choice, tool comparison and error interpretation put no sequence in
   the model's context. They route at `research-unpub` or `public`. See
   `classification_scope` in the ruleset.
2. **Somatic is in scope where the germline travels with it.** A tumour-normal
   pair contains a germline sample by construction and a tumour-only call set
   carries unfiltered germline variants, so somatic workflows classify here
   unless the material is demonstrably germline-free.
3. **Public, openly consented reference resources are not escalated.** They stay
   `public`. The escalate-when-arguable rule covers ambiguity about your own
   data, never published reference data.

Two questions the class does **not** answer, and they are open items #9 and #10:
which datasets carry consent or Data Use Certification terms permitting model
processing at all, even inside our own enclave; and whether an aggregation
(allele counts, cohort frequencies) genuinely lowers the class, at what cohort
size, determined by whom. Requesters will ask for that second route immediately.
It must not be answered ad hoc.

---

## Platform security tiers

| Tier | Platforms | Egress | Vendor retention | Audit trail | Validated |
|---|---|---|---|---|---|
| **S1** | Validated GxP instance | None | None | Part 11 complete | Yes |
| **S2** | Private research enclave | None | None | Application-level | No, unless qualified |
| **S3** | Commercial enterprise (Claude/OpenAI/Gemini) | Vendor | Contractual window | Vendor-provided | No |
| **S4** | M365 Copilot | Tenant-bounded | Tenant | Tenant | No |

**S3 is the tier that requires contract reading, not architecture review.** The
control is a term sheet: training exclusion, retention window, subprocessor list,
regional residency, deletion on termination. A SOC 2 report does not answer any
of these questions, and it does not cure a contractual transfer restriction.

**S4 is different in kind.** Copilot's risk is *reach*, not egress — it inherits
existing permissions and surfaces oversharing that already exists. The correct
control is tenant permission hygiene, which is an IT programme, not an AI one.

---

## HIPAA

| Control | Requirement |
|---|---|
| BAA | Required before any PHI reaches a vendor. **No commercial platform in this estate is routed for `clin-id`**, so no BAA is currently relied upon for routing. If that changes, the BAA precedes the routing change. |
| De-identification | Safe Harbor (18 identifiers) or Expert Determination. The determination artifact must be **attached to the workflow record**, not asserted. |
| Minimum necessary | Intake asks for the narrowest class that supports the work. |
| Audit | Intake log records class and verdict, never content. |

## GDPR and cross-border

| Control | Requirement |
|---|---|
| Lawful basis | Art. 9 special category requires an explicit basis. Consent for research is narrow and protocol-bounded — verify the use sits inside the consented scope. |
| DPIA | **Required** for any `clin-id` or `germline-seq` routing, for any `clin-deid` routing at scale, and for any new high-risk processing. `privacy-guardian` runs the trigger check. |
| Processor terms | Art. 28 terms with each vendor. Subprocessor list must be current. |
| Transfers | Chapter V. SCCs plus transfer impact assessment where data leaves the EEA/UK. |
| Pseudonymisation | Does **not** exit GDPR scope. The single most common misread in this matrix. |
| Jurisdiction axis | **Missing from the ruleset today** (open item #5). Several `clin-deid` cells likely split by jurisdiction. |

## EU AI Act

Application dates are phased and the classification question is live. Two
questions to put to counsel, not to this file: does any use case land in Annex
III high-risk, and what GPAI obligations attach to your deployment posture. The
portfolio's clinical use cases (29, 30) are the plausible candidates.

## Clinical trials

| Control | Requirement |
|---|---|
| ICH E6(R3) | Computerised systems used in trial conduct carry data governance expectations |
| Protocol scope | AI-assisted analysis must sit within the protocol and SAP, or be documented as exploratory |
| CRO agreements | The non-transferability question, per above. **Highest-value open item (#1).** |
| Sponsor accountability | Does not transfer to a vendor or a model. Ever. |

## GxP and Part 11

Any output entering a GxP record requires: attributability, audit trail,
qualification for the **specific context of use**, and change control over the
model version.

The consequence people resist: **a model version change is a change-control
event.** This is why the validated instance lags frontier versions, and that lag
is the price of qualification rather than a defect to engineer around.

## Export control and dual-use

Enclave containment does **not** resolve the deemed-export rule — access by a
foreign national inside your own boundary can still be an export. DURC/PEPP scope
requires institutional review upstream of any tool choice. Both route to the
Empowered Official; biology in scope adds the IBC.

---

## Access, retention, incident

- **Access:** routing is open to all staff (it holds nothing sensitive). Ruleset
  *write* access is restricted to the named owner. Approver actions are
  attributable to individuals.
- **Retention:** intake log retained per records schedule; contains no personal
  data. Eval results retain model outputs — **task packs must therefore contain
  no regulated data**, which is enforced by each pack's `data_policy`.
- **Incident:** an unmanaged-tool incident is triaged as an *intake coverage*
  failure, not a user-discipline failure. The question is why the routed path was
  slower or less useful than the unmanaged one.

## Controls that are asserted but not yet verified

Stated here so an auditor finds them from us rather than from a gap analysis:

1. No security, privacy, QA or legal reviewer has signed the matrix.
2. Vendor contractual terms are assumed from public positions, not read (#2).
3. No DPIA exists for any routed use case.
4. Enclave qualification status for GxP contexts is unknown (#3).
5. Deemed-export analysis for enclave access does not exist (#4).
6. Tenant classification accuracy for Copilot is unverified (#6).
7. No jurisdiction axis (#5).
8. The `germline-seq` conditional cells assume a consent and Data Use
   Certification answer nobody has produced (#9), and the class's tier placement
   is a judgement rather than a determination (#10).
