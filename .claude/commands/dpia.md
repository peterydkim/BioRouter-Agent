---
description: Run the DPIA trigger check and test the de-identification, consent-scope and transfer claims behind a routing request. Screens; never grants a lawful basis.
argument-hint: [the processing, e.g. "patient-trial matching on identifiable trial data, EU and US sites"]
---

Privacy screen: **$ARGUMENTS**

Invoke `privacy-guardian`. Read `docs/DATA-GOVERNANCE.md` and load
`.claude/skills/data-classification/SKILL.md`.

**No data enters this screen.** If the user pastes a record, an identifier, a
sequence or a document excerpt, stop and tell them to remove it — you need the
class, never the content. A privacy screen that ingests personal data has created
the processing it was asked to assess.

Test the de-identification claim before anything else. HIPAA de-identified is not
GDPR anonymous. Three questions: does a key exist anywhere, is any data subject
in the EU or UK, and is the determination artifact attached to the workflow
record? Any yes to the first two, or a no to the third, and it is `clin-deid`.
Genomic sequence does not de-identify at all — stripping identifiers from a VCF
does not lower its class, and that work is `germline-seq`.

Return the screening record:

```
DPIA_REQUIRED: yes | no | insufficient-information
basis / lawful_basis / consent_scope / transfer / transfer_tool /
processor_terms / approver
```

`insufficient-information` is a legitimate output. A `no` must name which
triggers were tested and why each failed to fire.

Then name the approver — **Privacy Officer / DPO, SLA 10 days** — and, where
provenance is in question, route the non-transferability question to Legal in
parallel. That is open item #1 and the highest-value one on the register.

State the ruleset's limitation when it bites: there is no jurisdiction axis today
(open item #5), so a `clin-deid` verdict may be a US-shaped answer to an
EU-shaped question.

Where the answer is "not at this class," say which class would work and what it
would take — aggregate to summary statistics, move to the enclave, or open the
DPIA with the DPO. A screen that returns only "no" produces the same outcome as
no screen at all, on a personal account, next week.
