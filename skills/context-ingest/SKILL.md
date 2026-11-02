---
name: context-ingest
description: "Save an explicitly authorized durable fact to the active memory system with deduplication and provenance."
---

# Context Ingest

## Select and authorize

Use only the active harness’s permitted memory system and destination. An explicit request or existing applicable authorization must cover the fact and its retention; finding stale information during recall is not authorization. Determine scope and whether synchronization or external access changes disclosure. Never store secrets, raw transcripts or unnecessary personal data.

Keep durable preferences, project decisions and constraints, useful feedback with its rationale, or pointers to external sources when they will change future work. Skip transient status, duplicates, facts easily recovered from code, and session-only details. A proposed global rule is not automatically a memory update.

## Deduplicate and save

Search the relevant index and matching entries first, using synonyms and domain terms; update a matching record rather than creating a duplicate when the system permits. Record a concise fact, source, scope, absolute date, uncertainty, and for feedback why and how it applies. Add relevant discoverability terms and links under the destination’s actual schema. Do not invent a common schema or path across providers.

Follow the store’s concurrency and write policy. If an index rebuild is required, verify whether a native hook actually ran; otherwise use the supported rebuild operation. Read back the saved record and verify the index when accessible. If the only permitted destination is an append-only note awaiting consolidation, describe that state without claiming propagation. For read-only lookup use [context-recall](../context-recall/SKILL.md), or search the store directly.
