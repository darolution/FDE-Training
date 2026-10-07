# Course rules

Six rules. They're also what a customer's security team will expect of you, so practise them from day one.

## 1. Only synthetic or public data

Every dataset in this course is either made up (fictional companies, people and `.example` web addresses, plus IP addresses reserved for documentation) or public.

!!! danger "Never use other people's data or systems"
    Don't point a lab at your employer's, a client's or your school's systems, and don't paste real emails, tickets, documents or personal details into a prompt, not even "just to test". Sending someone else's data to an outside service without permission can break workplace policy and privacy law, whatever your intention. If you want to try something at work, use the tools and approval process your organisation already has.

## 2. Secrets stay out of git

- API keys live in `labs/.env`. That file is git-ignored, so it isn't uploaded. Never paste a key into code, a notebook, a screenshot or a chat.
- Use a separate **course-only API key** with a **spend limit** (see [Costs](costs.md)).
- If you publish your own copy of the course, turn on GitHub's secret scanning push protection (see [Your own copy](setup/your-own-copy.md)).
- If a key ever leaks, **revoke it in the Console first**, then clean up. Revoking is what actually protects you.

## 3. Treat model input as untrusted

Customer messages, emails, documents, log lines and web pages can contain text written to trick an AI system ("ignore your instructions and…"). The datasets plant some on purpose. Your systems must treat that text as data: flag it, never obey it.

## 4. Don't switch off security checks to make something work

Some lab code refuses unsafe settings, for example skipping certificate checks on anything but your own machine. If a check blocks you, fix the cause, not the check.

## 5. Measure, don't assert

"It works" means "it passed the eval". From Phase 1, every capstone has acceptance criteria. Report the numbers, including the failures.

## 6. Know what things cost

Every API call made through the course's helper code is logged with its token count and cost. Check the usage report weekly. If spending jumps, something is probably looping.
