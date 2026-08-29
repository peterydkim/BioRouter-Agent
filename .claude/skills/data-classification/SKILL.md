---
name: data-classification
description: Place a piece of work on the thirteen-class routing ladder without ever seeing the data. Use when triaging an intake request, testing a de-identification claim, or deciding which of two arguable classes applies.
---

# Data classification

The class is the input to every routing verdict, so a classification error is a
routing error wearing a plausible answer. This skill is how you get the class
right from a description, never from the data itself.

## First: a class describes the prompt, not the subject

**Classify what enters the model's context and where the output goes. Never
classify the topic the scientist works on.**

"Write a Nextflow workflow for our WGS joint-genotyping run" puts no sequence in
the prompt: it is `research-unpub`, or `public` if nothing proprietary is
described. "Here are 200 variant calls from our cohort, interpret them" puts
sequence in the prompt: it is `germline-seq`. Same study, same scientist,
different class.

Getting this wrong in the cautious direction is not safe. It blocks pipeline
configuration, parameter choice, tool comparison and error interpretation —
most of what a bioinformatician actually asks — and it sends that work to a
personal account. The ruleset's `classification_scope` block is the governing
text.

## The ladder is a routing ladder, not a sensitivity score

Thirteen classes in `rulesets/ruleset.v1.json`, ordered by tier. **The tier is
not "how bad would a leak be."** It is how constrained the routing is, and
provenance can outrank content: CRO-sourced public method text can be more
constrained than internal unpublished results.

| Tier | Class | The trap |
|---|---|---|
| 1 | `public` | — |
| 2 | `internal` | — |
| 3 | `cci` | Retention, not access, is the usual gap |
| 4 | `predec` | Legal hold obligations attach |
| 4 | `research-unpub` | "No human subjects" must be verified, not assumed |
| 5 | `ts-chem` | Contractual no-training ≠ no-risk for crown jewels |
| 5 | `clin-anon` | True anonymisation is rarer than claimed |
| 6 | `clin-deid` | **Not GDPR anonymous** |
| 7 | `germline-seq` | Cannot be de-identified. Applies only when sequence is **in the prompt** |
| 7 | `pv` | Reporting obligation, not just confidentiality |
| 7 | `gxp-record` | **Destination, not origin, sets this class** |
| 8 | `clin-id` | — |
| 8 | `export-durc` | Enclave containment does not cure deemed export |

Always read the class list from the ruleset rather than from this table — the
ruleset is the maintained artifact and this is a reading aid.

## Ask in this order

**1. Where did it come from?** Provenance before sensitivity. "Where did this
data come from?" catches the Data Use Agreement problem that "is it
identifiable?" misses entirely. Partner, consortium and CRO data can be blocked
by contract at any identifiability level.

**2. Where does the output go?** Destination sets the class as much as origin
does. A prompt containing nothing but public method text lands in `gxp-record`
if the answer is pasted into a submission module, and in `pv` if it becomes part
of a case narrative. Ask explicitly: does this enter a regulatory submission, a
GxP record, a safety case, or a patient-facing decision?

**3. Is any human subject in it, and under what regime?** Then the
de-identification questions below.

**4. Which jurisdiction?** US, EU, UK, JP or multi. The ruleset has no
jurisdiction axis yet (open item #5), so record it on the tuple and flag that the
cell you read may be a US-shaped answer to an EU-shaped question.

## The four classification errors that cause incidents

### 1. "It's de-identified, so it's fine."

HIPAA §164.514 de-identification makes data non-PHI under US law. It does **not**
make it anonymous under GDPR — pseudonymised data remains personal data with a
full controller obligation. Three questions: does a key exist anywhere, is any
subject in the EU or UK, and is the determination artifact on file? A yes to
either of the first two, or a no to the third, means `clin-deid`, not
`clin-anon`.

### 2. "The prompt contains nothing sensitive."

See question 2 above. This is the error that intake catches only by asking about
destination, and it is the one users are most confident about.

### 3. "It came from our CRO, so it's ours."

Provenance outranks identifiability. Non-transferability clauses in partner,
consortium and CRO agreements can be breached by a prompt to a third-party model
**regardless of identifiability or vendor security posture**. This is the direct
analog of NIH's controlled-access genomic rule, and it is harder to see because
it is fragmented across many contracts rather than published in one notice.
Open item #1.

### 4. "We stripped the identifiers off the sequence."

Genomic sequence is re-identifying **in its own right**, and it identifies
relatives who never consented. HIPAA's eighteen Safe Harbor identifiers do not
list sequence data — a recognised gap in the rule, not a permission — while GDPR
Article 9 names genetic data explicitly. Removing a name from a VCF does not
lower its class. When that sequence is in the prompt, the class is
`germline-seq`, and there is no self-service route to it on any platform.

**Somatic work is in scope where the germline travels with it.** A tumour-normal
pair contains a germline sample by construction, and a tumour-only call set still
carries unfiltered germline variants. Classify a somatic workflow here unless the
material in the prompt is demonstrably germline-free — which is a claim to test,
not to accept.

**Public, openly consented reference resources are not escalated.** They are
`public`, and the tie-break below does not reach them.

Aggregate summary statistics — allele counts, cohort frequencies at a scale where
no individual genotype is recoverable — are a *different* class, and moving to
them is often the cheapest correct answer. Do not assert that a given
aggregation clears the bar; that determination belongs to the DPO. Say which
aggregation you are proposing and route it to `privacy-guardian`.

## Tie-breaking

**When two classes are arguable, take the higher tier and say you did.** The
rule reaches genuine ambiguity about *your* data. It does not reach published
reference data, and it does not reach a question that puts no regulated material
in the prompt. Escalating those is not caution, it is a routing error with the
same consequence as any other. Record
`confidence: low` so `ruleset-reconciler` can pick it up as an open item — a
recurring low-confidence pair is a taxonomy defect, and the register is where
taxonomy defects get fixed.

**Three clarifying questions maximum**, then commit to a class with a stated
assumption. A fourth round of clarification is how the tool gets routed around,
and an unrouted request becomes shadow AI. Classify high, flag the confidence,
and proceed.

## What never enters this process

The data. Not a record, not an identifier, not a sequence, not a file path to
regulated material, not a document excerpt. If it arrives anyway: stop, say
*"I only need the classification, not the content — delete that from the thread
and tell me what class it falls in,"* and do not quote it back. A governance tool
that ingests what it governs inherits every restriction it exists to route
around.

The intake log records the tuple and the outcome. **Never the request text** —
request text in a research organisation is itself sensitive.
