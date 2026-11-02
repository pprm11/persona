---
name: humanize
description: Rewrite a text so it reads well for a human, in the author's voice, with the meaning intact. One pass, no scorer, no agents. Use on /humanize, "humanize this", "make this read better", or before delivering any written piece. When the user asks for the heavy, full or scored version ("with the scorer", "does this sound AI-written?"), use `humanize-heavy` instead.
---

# Humanize

The goal is a text a human reads without effort and trusts. Fooling a detector is not the goal. Take the supplied text, rewrite it once with the checklist below, verify it against the original, deliver. No score, no subagents, no iteration loop. The scored pipeline lives in `humanize-heavy` and runs only when asked for.

## Input

- **The text.** Supplied in the skill argument or the message, or pointed to as a file. Without it, ask and stop. A calling skill may pass a bounded draft plus its immutable items (facts, numbers, links, IDs, paths, code). Never pull unrelated session history.
- **Instructions** (optional). Everything before a line containing only `---`, or a first line starting with `instructions:` or `rules:`. They override the defaults for this run. Meaning preservation changes only when the user says so explicitly. When a short opening line could be either an instruction or content, ask.

## The pass

Read the text once as its reader would. Then rewrite with these in mind:

1. **Lead with what the reader needs.** The answer, the decision or the ask comes first. Context follows.
2. **Cut what does not earn its place.** Filler, hedges ("it is worth noting"), formulaic connectors ("moreover", "in conclusion"), restatements, closing summaries, closing offers, empty adjectives, words a person would not say ("delve", "leverage", "seamless", "robust", "pivotal").
3. **Make it concrete.** Replace an abstraction with the fact, number, name or example the source already has. Never invent one. A claim without a source stays as it was or gets flagged to the user.
4. **One idea per sentence.** Vary length. Short sentences carry the point, longer ones the reasoning. Break "not X but Y" antitheses and triads built for rhythm rather than content.
5. **Structure for the reader.** Bullets only for parallel items, paragraphs for argument, a table when there are numbers to compare. Headers only in long text. Not every paragraph needs a tidy topic sentence, and the text does not need a moral at the end. Close on the concrete open item.
6. **Keep the voice.** Direct, plain, slightly informal, the way the author writes. No fake typos, no injected casualness, no slang the author would not use.
7. **House punctuation.** No dash as a pause (em dash, en dash, spaced hyphen), no semicolon, no colon in prose, no parenthetical aside, no ellipsis. Turn them into commas or separate sentences. Inline code, URLs, times, ratios and file names are exempt.

Three patterns are easy to miss. Drop the word that vouches for the text's own candor, as in "to be honest" or "the honest version", and state the point. Drop a frame that announces an insight, as in "the real question is" or "what this really means", and state the finding. Drop a closing offer such as "if you want, I can also do X", and end on the pending step. Keep an offer when the next step is required or the user asked for options, and keep a caveat that carries content, with only its label removed.

Revise the flagged passages. Do not regenerate the whole text, that brings the same tics back.

## Preserve

Meaning, facts, numbers, links, IDs, citations, code, product names, technical terms, and the input language (Portuguese stays Portuguese, English stays English). Changes to substance happen only within what the user explicitly authorized. After rewriting, read the original once more and confirm nothing was lost or added.

## Deliver

1. **The final text**, in a fenced block, ready to copy. For a composed call, return the revised text to the calling skill instead. The caller owns presentation and the genre specific source audit.
2. **One or two sentences** on what changed and which instructions were applied.

When the user wants a number or a detector pass, say this pass has none and offer `humanize-heavy`.

## Related

- [[humanize-heavy/SKILL|humanize-heavy]]: the scored pipeline (60 point script plus a 3 agent rubric), on request only
