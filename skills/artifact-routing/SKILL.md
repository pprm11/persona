---
name: artifact-routing
description: Route a document, HTML page or diagram to its Diataxis type (tutorial, how-to, reference, explanation), one type per tab when they share a page, then write, build and check it. Other media use the same routing plus a medium skill. Use when drafting or revising an artifact.
---

# Artifact routing

This skill decides HOW an artifact is shaped, written, built and checked. It does not decide WHICH documents a project needs or what each must contain: that belongs to a genre skill (for example a staged engineering series, an RFC, an ADR, a PR description, a task card). When a genre skill calls this one, reuse its brief and return the routing decision; do not call it back.

Apply the routing when creating or materially redesigning an artifact. For a small edit, keep the existing artifact and scope and classify only for the handoff line. Keep the requested medium, format and constraints. A requested draft does not authorize publishing or any other external action.

## Three axes, one owner each

| Axis | Question | Owner |
|---|---|---|
| Type | What does the reader need to do with this part: learn, act, look up, understand? | this skill, `references/<type>.md` |
| Genre | Which document is it and what must it contain (RFC, ADR, runbook, API reference, test plan)? | the genre skill, if any; otherwise the skeletons in the type files |
| Medium | Page, deck, sheet, diagram, chat reply | this skill for pages (`reader-page.md`); a medium skill for the rest |

## Identify the reader and the use

Infer the reader and the occasion from the request and from direct evidence about the reader. A role or title alone does not prove familiarity. Requester, reader, reviewer, decider and maintainer can be different people; separate them when it changes the result. If a material ambiguity cannot be resolved, ask one precise question; otherwise proceed with the best-supported reading and say what you assumed.

## Pick the type, per part

Every part of an artifact gets exactly one of four types, chosen by the outcome the reader needs and the acceptance check, never by file format or genre. The four come from [Diataxis](https://diataxis.fr/); applying them to every artifact (code, visuals, decks, sheets) is this skill's adaptation.

| Type | The reader | Accepted when | Read |
|---|---|---|---|
| Tutorial | learns by doing a guided, safe exercise | the learner reaches the promised outcome and can repeat it | `references/tutorial.md` |
| How-to guide | gets a real task done | the task is done and verified under the stated conditions | `references/how-to.md` |
| Reference | looks up a reliable fact | the reader finds the property and reads it correctly | `references/reference.md` |
| Explanation | understands why, how it fits, what the trade-offs are | the reader can state the relationship and its limits, or decide | `references/explanation.md` |

There is no fifth type. A diagram that helps locate properties is Reference; one that shows causality is Explanation; an executable tool that does a task is a How-to; a ready-to-use asset is classified by its practical use and delivered without tutorial text.

## One artifact, several types in tabs

When one reader on one occasion needs more than one type (for example install it, look up a flag, understand why), build one page with one tab per type instead of mixing them in one flow.

- Each tab has exactly one type, its own skeleton and its own acceptance check. Do not let explanation leak into how-to steps or instructions into reference tables; move it to the right tab and link.
- Order the tab bar Tutorial, How-to, Reference, Explanation, and leave out tabs with no real content. The default tab is the reader's main job and need not be the first: mark it with `aria-selected="true"` and leave its panel without `hidden`.
- Tabs link to each other with in-page anchors; a link into a hidden tab opens it (the reader script does this).
- Split into separate artifacts when audience, occasion or access differs. Preserve the user's scope; propose a split instead of expanding silently.

## Shared references

| File | Use it for |
|---|---|
| `references/skeletons.md` | section skeletons for README, runbook, install guide, API and CLI reference, RFC, ADR, postmortem, each mapped to a type |
| `references/components.md` | building blocks: In one minute, as-of and What changed, IDs, open questions, decisions, evidence and citations, privacy, pending notices, success checks, failure tables; the scripts |
| `references/writing.md` | readability by level: document, section, paragraph, sentence, clause, word; content protection |
| `references/ubiquitous-language.md` | choosing, defining and keeping terms; the glossary as the single source |
| `references/linking.md` | what becomes a link, anchors, cross-tab links, permalinks, `scripts/autolink.py` |
| `references/diagrams.md` | captions, legends, size limits, which diagram per type, mermaid pitfalls |
| `references/reader-page.md` | the HTML page: shell, markup contract, reader features, artifact limits, how to check |
| `references/quality-gates.md` | well written, correct, optimized: who checks, finding format, pass and stop rules, per type |
| `references/source-isolation.md` | separate audiences with separate access in one request |

Templates: `assets/templates/shell.html` (base page), one worked example per type in `assets/templates/<type>.html`, and `multi-type.html` (four tabs on one sample product). Reader: `assets/reader/reader.js` and `reader.css`.

Reading order for a new artifact: this file, then the type file of each part, then `skeletons.md` if the document has a known genre and no genre skill covers it, then `components.md`, `writing.md` and `ubiquitous-language.md` while writing, then `reader-page.md`, `linking.md` and `diagrams.md` when building a page, and `quality-gates.md` before handoff.

## Produce

1. Write the reader, the use and each part's type. Write the answer of the artifact in one sentence; if you cannot, there is a content gap: ask.
2. Gather sources. Every number and claim needs one; `components.md` says what to do with a claim that has none.
3. Fill the type skeleton (or the genre skill's content contract) with the components it calls for. Build the glossary first; it feeds popovers, search and links.
4. Write with `writing.md` and `ubiquitous-language.md`, then run a style pass if one is available to you (for example a `humanize` skill). Use the scored `humanize-heavy` workflow only when explicitly requested or required by the calling workflow; if unavailable, report the scored check as not run. Do not run a prose style pass on code, data or visuals.
5. For a page, follow the build steps in `reader-page.md`: write a lean source with the reader markers empty, build it with `scripts/build_page.py --autolink`, check it, and look at it once in light, dark and phone width. For hand-drawn SVG labels, run `scripts/svg_gate.py` and inspect the actual rendering; its width estimate is not a visual measurement.

Use a medium skill when one fits (slides, sheets, PDF, images) and an iterative research skill for evidence gaps, by name, when your layers have them.

## Verify

Run the three gates in `quality-gates.md` sized to the stakes: a cold reader with an answer key for "well written", an adversarial check of every claim against its source for "correct", and "does each part need to exist" for "optimized". For consequential prose, map each claim to its evidence before handoff, including claims of absence, resolution, cause and commitment; test an alternate scenario consistent with the facts to catch unsupported universal claims. State limits and unverified items plainly. Respect access and permissions for sources and outputs.

## Handoff

In chat, one line per artifact in the user's language: audience, intended use with a verb, and type (or the type of each tab). Example: `Audience: new operators · Use: produce a quote · Type: How-to guide`. Keep this line out of the artifact and out of strict machine-readable output.
