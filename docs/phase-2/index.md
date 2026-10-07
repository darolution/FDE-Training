# Phase 2 · Production building blocks

**Weeks 5–10 · not yet written.** This page is the plan. Lessons and labs land here when Phase 1 is done.

**Capstone 2: Northwind Outfitters support agent.** An agent that answers customers using tools: order lookup, a refund tool that **requires human approval** above $200, policy retrieval with citations, and escalation. It's judged by an eval of 40+ conversations and a red-team report.

| Week | Topic | Key outcomes |
|---|---|---|
| 5 | Claude Code as an FDE tool | CLAUDE.md for a customer repo, a custom skill, hooks for guardrails and logging, subagents, `claude -p` in CI. **Portfolio project:** guardrail hooks that detect bypasses (for example, `cat`/`head` via Bash skipping a `Read` hook) and log decisions to Splunk, with tests and a write-up |
| 6 | Tool use | Tool schemas, strict tool use, parallel calls, writing the agent loop yourself, handling tool errors |
| 7 | Documents and retrieval | Long context vs RAG, chunking, contextual retrieval, the Files API, citations |
| 8 | Integrations | REST, webhooks, OAuth client credentials, idempotency keys, retries, Message Batches for bulk work |
| 9 | Agent security | Threat-modelling prompt injection, least-privilege tools, approval gates, output encoding. *Security track: red-team a SOC triage agent with the planted log injection* |
| 10 | Capstone 2 | Discovery → build → evals → red team → handover |

Read ahead: [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · [Claude Code docs](https://code.claude.com/docs/en/overview) · [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
