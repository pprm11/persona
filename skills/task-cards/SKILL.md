---
name: task-cards
description: "Turn a plan into actionable task cards with observable acceptance criteria and dependencies."
---

# Task Cards

## Prepare

Read the plan and its cited evidence before dividing work. Order tasks by dependencies and identify overlapping writers. Each card has one outcome that a cold reader can begin and verify. Distinguish the card text from a ticket in a tracker; preparing cards does not create tickets.

A wide change that breaks consumers that build or deploy separately uses expand-contract. One card adds temporary compatibility (old and new interface both work, behavior unchanged). Migration cards move consumers in batches, and each batch passes its gate with both interfaces present. A separate removal card depends on every migration card, states what shows that no consumer is left, and deletes the compatibility. A change stays one card only when it ships atomically, with every consumer (one or many) built and deployed together with it; a compatibility layer there only adds code to delete later. A single consumer that deploys on its own schedule still needs the compatibility card.

## Card

Give each card a result-oriented title; a short, sourced problem; scope and deliverables; observable acceptance criteria with commands and expected outcomes where known; relevant guidance and a test or gate that detects recurrence; dependencies or external blockers; and likely files when known. Cite the exact ref and commit when a cited file exists only on another branch. Mark a product decision as an open question or blocker when the executor lacks authority; do not invent an owner, fact or estimate.

An acceptance criterion such as “works” is insufficient. A meaningful negative control can show that the gate fails on the defect it is meant to detect. Reuse existing guidance and sensors when they already cover a refactor.

## Review and delivery

Have a cold reader check whether they can start, run the acceptance checks, locate the sources and understand dependencies. If independent review is unavailable, apply the checklist yourself and disclose the limitation. Correct failures and recheck them; stop after three rounds or two repetitions of the same unresolved failure and surface the question. Provide an ordered dependency table with the cards. Create or update tracker items only within the user’s authorization, checking for duplicates first. For presentation use [artifact-routing](../artifact-routing/SKILL.md) if installed; otherwise adapt to the reader.
