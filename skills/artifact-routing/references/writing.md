# Writing rules, level by level

Use this file when you write or revise the text of any artifact, whatever its Diataxis type. Work from the top level down: fix the document first, because restructuring removes many faulty sentences before you polish them. Each rule has a one-line before and after. Rules are defaults for readers who skim, check and act; a short note needs far fewer of them.

## 1. Document level

### Answer and ask first

- Open with the answer, the ask, the numbers that decide, and what is still open and with whom.
- Before: "This document reviews the retry options we looked at over the quarter."
- After: "Use exponential backoff with jitter. We need approval by 2026-03-12. One question is open: the cap for batch jobs."
- Revised documents add a short "What changed in revision N" under the summary, one line per change, naming the decision or question it closes.

### The headings test

From the title, the first paragraph and the headings alone, a reader must be able to say what was decided, what is asked, by when, and where each detail lives. Run this test before you ship. If it fails, rewrite the headings, not the body.

### Headings that state the claim

- Before: "Considerations".
- After: "Read replicas do not reduce write contention".
- Keep a template name where readers expect it (Summary, Open questions), and make the first sentence under it the claim.
- Use plain noun phrases for reference material that readers look up by name (a field, a flag). Use verb phrases for tasks ("Rotate the signing key"). Use claims for explanations.
- One topic per heading. Two levels of depth is normal, three is the limit for a page; a fourth level means the section should be its own tab or document.

### One summary

- Put one summary at the top. Do not add an intro that lists the sections, a "Key takeaways" box, or a conclusion that repeats the top.
- Close on the next action or the open item, not on a moral.

### Scale structure to length

- A note of a few paragraphs needs a clear first sentence, not a summary plus claim headings that repeat it.
- A revision is usually shorter than the original. It grows only when you add something the reader needs, such as a missing step or an explicit condition.

### Choose the format by the shape of the content

| Content | Format |
|---|---|
| Reasoning, cause, contrast, trade-off | Prose |
| Ordered actions | Numbered steps, one checkable action each |
| Parallel items of equal weight | Bullets |
| Items that share three or more attributes, each cell a final answer | Table |
| Conditions with several "or" or "not" branches | Decision table or flowchart |

- Introduce every list and table with one sentence that says what it shows.
- Bullets that carry reasoning but no "because" should become prose.
- Before: a table whose cells say "depends".
- After: a decision table with one row per condition and a concrete outcome in each cell.

### Sections that stand alone

Readers jump in from a link, a search hit or a retrieval system, and a retrieved section arrives without its neighbors.

- Name the subject again instead of "it" or "as above" at the start of a section.
- State critical facts in prose as well as in a table.
- Keep each section answerable on its own: what it is about, what it concludes, what it depends on (with a link).

### Language and dates

- Write the whole artifact in one language, labels and captions included.
- Date anything that can go stale ("as of 2026-03-01"). Use absolute ISO dates (YYYY-MM-DD) in dated records, in one format across the artifact. In living pages avoid "currently", "new" and "soon".
- Put a source on every number and claim: a file and line, a link, a command, a ticket.

## 2. Section and paragraph level

### One point per paragraph, stated first

- The first sentence is the point. The rest supports it.
- Before: "There are many things to say about caching. We tried several approaches. The shared cache won."
- After: "The shared cache won, because it cut p95 latency on the read path. We also tried a per-process cache and a CDN rule."

### Given-new order

Start each sentence with something the reader has just seen and end with what is new. This links sentences without connectors.

- Before: "A queue sits between the API and the worker. Ordering is guaranteed per tenant by it."
- After: "A queue sits between the API and the worker. The queue guarantees ordering per tenant."

### Connectors only when they state a relation

- Keep because, so, but, unless, therefore.
- Delete Moreover, Furthermore, Additionally, In conclusion.
- Before: "Moreover, the cache expires after 60 s."
- After: "The cache expires after 60 s."

### Delete padding, keep argument

| Pattern | Fix |
|---|---|
| Throat-clearing ("It is worth noting that") | Start with the claim |
| Restated verdict at the paragraph end | Delete it |
| Editorializing ("an important decision") | State the consequence: "If this is wrong, rollback takes two weeks" |
| Fabricated contrast ("not just a gateway, the backbone") | Say what it is and does |
| Automatic triplet ("faster, safer, simpler") | Keep only what you can support |
| Balance with no position ("both have pros and cons") | State the deciding criterion, or say no decision exists |

### Mechanism check and disproof check

- Mechanism check: for every "ensures", "enables", "improves", "handles", "supports", say by what mechanism and when it fails. If you cannot, delete the claim or mark it as unknown.
- Disproof check: could anyone show the sentence wrong? If not, add a number, a name or a limit.
- Before: "This approach ensures scalability."
- After: "Each shard handles one tenant, so load grows with tenant count; a single tenant above 10k requests per second still saturates its shard." (numbers must come from your source)

## 3. Sentence and clause level

- **Keep the subject next to its verb.** Before: "The service, which after the refactor handles retries for all clients, times out after 30 s." After: "The service times out after 30 s. Since the refactor, it handles retries for all clients."
- **Split chains of which, where and being that.** Each one becomes a new sentence with its own subject.
- **Put the condition before a destructive or costly action.** Before: "Restart the workers if lag is above 5,000." After: "If lag is above 5,000 and consumers are 0, restart the workers."
- **Limit stacked nouns to three.** Before: "session token refresh failure alert threshold". After: "the alert threshold for failed session-token refreshes".
- **Replace hidden verbs.** Before: "Perform a validation of the payload prior to insertion." After: "Validate the payload before you insert it."
- **Replace stacked negation.** Before: "Do not disable X unless Y is not set." After: "If Y is set, keep X enabled. If Y is not set, you can disable X."
- **Resolve ambiguous pronouns** by repeating the noun. Before: "The proxy forwards to the worker and it retries." After: "The proxy forwards to the worker and the worker retries."
- **Use the agentless passive only when the actor does not matter.** Before: "It was decided that the flag stays off." After: "The release owner decided the flag stays off." Blameless incident writing is a valid use of system subjects.
- **Treat 25 words as an alarm, not a law.** Look hard at any longer sentence, and keep the "because" when you split.
- **Mean it with MUST, SHOULD, MAY only in specifications.** In procedures write "must" and "can", and avoid "should".
- **Avoid objects that act like people.** Before: "The orchestrator decides which agent wins." After: "The orchestrator routes the message to the agent with the highest intent score."
- Avoid trailing "-ing" chains. Before: "It returns a dict, enabling callers to filter." After: "It returns a dict. Callers can filter it."

## 4. Word level

- **Plain verbs.** use not utilize, start not commence, choose not select from amongst.
- **Exact numbers and units.** Before: "a short timeout". After: "a 30 s timeout".
- **Absolute dates** in dated records.
- **One term per concept.** Never vary a term for style; see `ubiquitous-language.md`.
- **AI marker words** (delve, leverage, seamless, pivotal, robust, comprehensive, ecosystem) matter by density. Do not hunt single words; reduce clusters.
- **Expand acronyms on first use** in each artifact, and do not define one you use once. Common ones (HTTP, API, JSON, URL) need no expansion. On the page, mark the first use with `<abbr title="...">`.
- **Phrasal verbs for global readers.** Prefer single verbs: find out becomes determine, look into becomes investigate, kick off becomes start. Established technical terms (log in, set up) stay.
- **Optional profile: false cognates for writers whose first language is Portuguese or Spanish.** Use it when the author group fits; skip it otherwise. Watch these:

| Wrong | Right |
|---|---|
| actually (meaning "now") | currently, or "as of <date>" |
| eventually (meaning "possibly") | sometimes, possibly |
| pretend to ship | plan to ship |
| a doubt about | a question about |
| assist the meeting | attend the meeting |
| evidences, informations, feedbacks | evidence, information, feedback |
| depend of, associated to | depend on, associated with |
| make the deploy, perform the implementation | deploy, implement |

- Machine translation: keep sentences near 25 words or fewer, spell and capitalize each term the same way every time, and keep pronouns in the same sentence as their referent.

## 5. Code samples, tables, captions and alt text

### Code samples

- Every sample runs as pasted. Placeholders are written in capitals and explained right below the block.
- Show the expected output next to the command, or mark that there is none.
- Name the language on the fence. Keep samples short enough to read without scrolling sideways; link to a file for long ones.
- Put recovery notes next to the step that can fail: "If you see `connection refused`, the pod is still starting; wait 30 s and repeat step 4."
- Test samples in CI when you can. Pin the version they were checked against.
- Never edit inside a code block while you revise prose.

### Tables

- A table needs a header row, one sentence of introduction and a stable column order. Every cell is a final answer or an identifier, never "see below".
- Keep tables under about 7 columns at 400 px width, or let them scroll inside their own container.
- Repeat a critical table fact in prose.

### Captions and alt text

- A caption says what the figure shows and what to notice. A legend states what each colour or arrow type means.
- Alt text states the point of the figure in one or two sentences ("Requests pass the cache first, then the database; only writes reach the queue"). Do not write "diagram of".
- Decorative images get empty alt text.
- Link text is the title of the destination, never "here" or "see section 9".

## 6. Content protection

When you rewrite or review, these rules come before every style rule.

1. Never invent facts. For a claim with no source, apply the table in `components.md` (Evidence and citations, "A claim with no source"), and ask the author for a missing fact in your reply.
2. Preserve numbers, dates, units, commands, flags, identifiers, tags and code byte for byte.
3. Never decide what the document has not decided. If the status is "in discussion", keep it and ask who decides and when.
4. Keep the reasoning, the rejected alternatives, the known limits and the conditions. Compare every warning before and after the edit.
5. Do not over-correct. A list of three that really is three, a passive in a blameless record or a long sentence that reads well can stay.
6. Do not add empty template fields the author did not write. Recommend them in your reply.

## 7. Checks

Run them in this order after any substantial edit.

| Check | How |
|---|---|
| Fact preservation | Diff the numbers, identifiers, tags and code blocks between the original and the revision (a small script that extracts them and compares sets is enough). Any difference must be intended. |
| Readability pass | Four passes in order: document, paragraph, sentence, word. Sections 1 to 4 of this file are the checklist for each pass; a readability skill such as `technical-doc-readability` adds evidence, if you have it. |
| Style | Run your style skill (for example `humanize`, if installed). Punctuation bans such as no dash as a pause, no semicolons, no colons or parentheses in prose are an optional personal profile, not a default of this skill. |
| Cold reader | A second reader with no context answers the acceptance questions of the tab from the text alone. Every wrong answer points to hidden context. |
| Evidence of tests | A checklist alone misses problems that real readers hit, so a cold read decides. |

When review rounds keep finding new problems, apply the stop rule in `quality-gates.md`.
