---
name: decision-rfc
description: "Write a decision RFC describing a sourced problem, options, tradeoffs and open questions."
---

# Decision Rfc

## Establish the decision

This applies when a decision is pending. A comparison of existing systems where nothing is being chosen calls for an explanation document and needs none of the scaffolding below. Identify the reader, decision owners, question, constraints and whether a recommendation is requested. Read relevant code at a fixed ref, decision records and authoritative sources. State the date or commit for time-sensitive evidence. Where a source is inaccessible or absent, mark the claim as unknown or an open question instead of inventing a fact.

## Draft

Use the repository’s RFC style if it exists. Otherwise write a decision-oriented title, status and owners, followed by problem, goals and non-goals, relevant context, viable options, open questions and next steps ordered by dependency. Goals say what a good outcome must satisfy; non-goals name what the decision deliberately leaves unchanged. Explain each option and its pros and cons in comparable terms, including its cost (build and operating, from a cited source or marked as an estimate with its basis, otherwise an open question, with an owner when one is known) and its fallback (what survives, or how to back out, if that option fails). Include the status quo when viable. Provide a recommendation only when requested or appropriate to the decision authority, with its rationale and what would change it; when others decide, strip verdict labels such as "recommended" or "final" inherited from source material. The author and decision owner can differ.

Use concise prose and tables where they improve comparison. Cite factual claims close to the claim, state limitations, and avoid estimates without a stated basis. If the document is part of a multi-stage series, [staged-engineering](../staged-engineering/SKILL.md) owns the series; if unavailable, trace later designs back to the decisions here.

## Check and hand off

A reader without the conversation should be able to assess the options and identify the unresolved decisions. Recheck sources after editing or a style pass. Drafting alone does not publish or apply the decision. Use [artifact-routing](../artifact-routing/SKILL.md) for presentation when installed; otherwise fit the document to the reader and requested medium.
