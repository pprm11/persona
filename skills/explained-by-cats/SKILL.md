---
name: explained-by-cats
description: Turn a document (RFC, briefing, architecture plan, proposal) into a short vertical "explained by cats" reel, either an interactive 9:16 HTML story page with drawn kittens or a narrated script, where every scene pairs a cat metaphor with a plain translation back to the real thing. Use when the user asks for a reels, stories or kittens version of a document, or a playful explainer for a non-technical audience.
---

# Explained by cats

A reel retells one document in 8 to 12 scenes. Each scene shows cats doing something familiar and ends with a **Translation** line that says, in plain words, what the scene means in the source. The cats carry attention; the translation carries the content. A scene without a translation is decoration and gets cut.

## Inputs

- The source: a link, file or pasted text. Read all of it before writing. If it is behind a sign-in, ask the user to open it; do not guess the content.
- The format, if the user names one: **page** (interactive HTML, the default) or **script** (narration, on-screen text and shot list for someone to film or animate).
- The language: the source's language unless the user asks otherwise.

## Steps

1. **Pick the spine.** From the source, take one sentence for "what this is" and the 6 to 10 points a reader must leave with: the problem, the key numbers, the decision or flow, the risks, the deadline, the rules. Drop everything else; the reel links back to the source.
2. **Find one metaphor per point.** Use household cat situations people already know: the feeder that releases food on a schedule (a fixed rule the cat cannot talk past), knocking a glass off the table (a small per-step error that adds up), a cat tree with floors (layers), a bell on each collar (tests that point to the culprit), the front door (an irreversible action that needs a human), a cat that will not fit in the box (overclaiming), the mother carrying kittens (one party responsible for the others). Reuse a metaphor across scenes only when it is the same idea.
3. **Write each scene** as: eyebrow (2 to 4 words), headline, one or two short sentences in cat terms, then `Translation:` with the real meaning. Numbers, names, dates and thresholds come from the source, verbatim. Never invent a number to make a joke land; if the source has none, the scene has none.
4. **Order:** hook (the problem in one line), today's pain, the ideas or flow, the hard rules and risks, the plan or deadline, and a last scene that links to the full document and any companion versions.
5. **Build it.**
   - **Page:** copy [assets/reel-template.html](assets/reel-template.html), replace its example slides, keep its player (progress bars, tap left or right, hold to pause, arrow keys and space), the three cat faces (`#cat` open, `#catz` sleepy, `#cato` startled) and the fur colours. Set the header handle and the caption to the subject. Load the platform's page-design guidance before publishing when it has one.
   - **Script:** per scene give the time range, the shot (what the cats do), on-screen text and narration. Aim for 60 to 90 seconds; the first scene must hook in the first 3 seconds.
6. **Check before delivery:** every number traces to the source; every scene has its translation; the copy reads like a person wrote it (run `humanize` if installed). Open the page at a small phone (375x667), a tall phone (375x812) and a desktop window, and confirm on every slide that no element overlaps another, the header or the caption. The template's fit guard (no flex shrink, `safe center`, zoom down to 60%) prevents overlap; if a slide still needs zoom below 0.9, split it instead of shrinking it.

## Confidentiality

A reel spreads further than the document it explains. If the source is marked internal, confidential or "do not share", or names clients, prices or people, deliver the script in chat or as a local file, and publish a page only after the user confirms who may see it. Do not carry figures from other clients or other documents into the reel.

## Do not

- Do not let the metaphor change the meaning: if a scene's translation says something the source does not, rewrite the scene.
- Do not use photos or copyrighted characters; the drawn faces in the template are enough.
- Do not stack more than three lines of body text on a slide; split the scene instead.
