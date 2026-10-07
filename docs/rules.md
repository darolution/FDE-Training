# Course rules

Six rules. Most of them are what a customer's security team will ask of you anyway, so practise them now.

## 1. Only synthetic or public data

Every dataset in this course is synthetic (generated or hand-written, with fictional companies, people, `.example` domains and documentation IP ranges) or public.

!!! danger "Never use employer data or systems"
    Don't point a lab at your employer's Splunk, Sentinel, ticketing or any other system, and don't paste work logs, tickets or documents into a prompt, even "just to test". Sending employer data to an external API from a personal project can breach data-handling policy and law, whatever the intent. If you want to pilot something at work, go through your employer's approved AI tooling and review process.

## 2. Secrets stay out of git

- Keys live in `labs/.env`, which is git-ignored. Commit `.env.example`, never `.env`.
- Use a **course-only API key** in its own Console workspace with a **monthly spend limit**.
- Turn on GitHub secret scanning push protection for the repo (see [workflow](setup/workflow.md)).
- If a key ever lands in a commit, **revoke it first**, then clean up history. Revocation is what actually protects you.

## 3. Treat model input as untrusted

Tickets, emails, log lines and web pages can contain text written to manipulate an AI system. The datasets plant some on purpose. Your systems must treat that text as data: flag it, never obey it.

## 4. No TLS shortcuts outside localhost

The lab code refuses `SPLUNK_VERIFY_TLS=false` unless the host is a loopback address. Don't work around that check. In a customer environment, use their CA bundle.

## 5. Measure, don't assert

"It works" means "it passed the eval". Every capstone has acceptance criteria. Report the numbers, including the failures.

## 6. Know what things cost

Every API call made through `fde_common.llm` is logged with tokens and dollars to `labs/runs/usage_log.jsonl`. Check the log weekly. The whole course should cost tens of dollars, not hundreds. If it doesn't, something is looping.
