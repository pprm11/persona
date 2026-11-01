# Seed A: outbound message queue (test seed, not a real task)

Use the skill `staged-engineering` to do this task.

Investigate where an outbound sending service for the Acme order assistant (templates and follow-ups) should run, shared by v1 and v2 during the canary. Today each version sends straight to the messaging provider, and the line has a rate limit; with both sending at the same time, we may exceed the limit or send two messages to the same customer. Write the whole series: problem domain, as-is, market study, solution domain, HLA and HLD. Analyze cost, do the 1-3-1 and decide. Evaluate technologies and decide. You may build POCs to test the concepts.

Not allowed: deploy, creating cloud resources, changing config, commit, push, opening a PR, sending a message to anyone. Read-only on every system. Do not print secrets.

Setup for this test run:
- Repository: the current folder is a checkout of `acme-org/order-assistant`. Read code only at commit `abc1234` (`git show abc1234:<path>`).
- The as-is may use files and public documentation only. No live checks against any cloud, database or API in this test: write NOT VERIFIED where a live check would be needed, with the command that would verify it.
- Write every output under `skill-test/` in the current folder. Do not touch any other file.
- Owner answers: when your problem domain draft lists its questions for the owners, and only then, read `answers-a.md` (next to this seed, path given in your task message). Those are simulated owner answers for this test. Apply them as the skill says.
- Prices: the AWS public price list JSON files may be downloaded with curl from `https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<Service>/current/sa-east-1/index.json` into `skill-test/prices/`.
- When done, write `skill-test/REPORT.md`: what you produced, what you could not do, and every place where the skill's instructions were unclear or missing.
