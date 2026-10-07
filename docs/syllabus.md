# Syllabus

**From zero:** Launchpad (8 weeks) + Phases 1–5 (24 weeks) = about **32 weeks**.
**If you already code:** start at Phase 1, about **24 weeks**.

Plan on roughly **8–10 hours a week** for Launchpad and **10–15 hours a week** from Phase 1. Each part opens with a **checkpoint** so you can skip what you already know, and from Phase 1 each phase closes with a capstone for a new customer.

!!! abstract "What an FDE needs, and where it's covered"
    | Skill | Where |
    |---|---|
    | Terminal, Python, Git/GitHub, HTTP and JSON, testing | Launchpad L1–L7 |
    | Claude API, models, cost, latency | Weeks 1, 19 |
    | Prompting, structured outputs, caching | Week 2 |
    | **Evals**: proving a system works | Week 3, every capstone |
    | Claude Code as a delivery tool (CLAUDE.md, skills, hooks, subagents, headless) | Launchpad L7, Week 5 |
    | Tool use and integrations | Weeks 6, 8 |
    | Retrieval, long context, documents, citations | Week 7 |
    | Agent security and prompt injection | Week 9, every capstone |
    | Claude Agent SDK, multi-agent patterns, context management | Weeks 11, 14 |
    | MCP servers, local and remote, with auth | Weeks 12, 13 |
    | Observability and operations | Week 15 |
    | Enterprise deployment, cloud platforms, data residency | Weeks 17, 18 |
    | Shipping: services, containers, CI, human review UIs | Week 20 |
    | Discovery, scoping, demos, change management, writing | L8, Weeks 4, 10, 16, 21, 22 |

## Launchpad · for beginners (L1–L8) ✅ written

| Week | Topic |
|---|---|
| L1 | [Your computer as a workshop](launchpad/l1-terminal.md): terminal, files and folders, installing tools, VS Code |
| L2 | [Python 1](launchpad/l2-python-basics.md): values, variables, text, numbers, running scripts |
| L3 | [Python 2](launchpad/l3-python-data.md): lists, dictionaries, loops, decisions, functions |
| L4 | [Python 3](launchpad/l4-python-files.md): files, JSON, errors, packages, virtual environments |
| L5 | [Git and GitHub](launchpad/l5-git.md): commits, branches, pushing, forks, keeping secrets out |
| L6 | [The web and APIs](launchpad/l6-apis.md): HTTP, calling an API from Python, keys and environment variables |
| L7 | [Working with AI tools](launchpad/l7-ai-tools.md): Claude and Claude Code as a coding partner; testing with pytest |
| L8 | [Launchpad project](launchpad/l8-project.md): a small tested command-line tool on GitHub |

## Phase 1 · Foundations (Weeks 1–4) ✅ written

| Week | Topic | Labs |
|---|---|---|
| 1 | [Claude API essentials](phase-1/week-01.md): messages, models, tokens, cost, streaming, errors | First call, token counting, streaming, error zoo, multi-turn cost, usage report |
| 2 | [Prompting for real work](phase-1/week-02.md): system prompts, structure, structured outputs, caching | Prompt ladder, ticket triage, caching. *Security track: alert triage* |
| 3 | [Evals](phase-1/week-03.md): golden sets, code graders, LLM-as-judge, regression gates | Eval runner, run diff, calibrated judge |
| 4 | [Capstone 1: Claims intake for Lakeshore Mutual](phase-1/week-04-capstone.md) | Discovery → extractor → rules → evals → security review → handover |

## Phase 2 · Production building blocks (Weeks 5–10)

| Week | Topic |
|---|---|
| 5 | **Claude Code as an FDE tool**: CLAUDE.md, skills, hooks, subagents, headless mode in CI. **Portfolio project: guardrail hooks.** Hooks that enforce file-access rules, detect bypasses (for example, `cat` or `head` via Bash reading a file that a `Read` hook would block) and log every decision to a local file. *Security track: send the log to Splunk* |
| 6 | **Tool use**: tool schemas, strict tools, parallel calls, the agent loop, tool errors |
| 7 | **Documents and retrieval**: long context vs RAG, chunking, contextual retrieval, the Files API, citations |
| 8 | **Integrations**: REST APIs, webhooks, auth, idempotency, retries, Message Batches for bulk work |
| 9 | **Agent security**: prompt-injection threat modelling, least privilege, approval gates, output handling. *Security track: red-team an alert-triage agent* |
| 10 | **Capstone 2: Northwind Outfitters support agent**: order lookup, refunds behind human approval, policy retrieval, escalation, evals and a red-team report |

## Phase 3 · Agents and MCP (Weeks 11–16)

| Week | Topic |
|---|---|
| 11 | **Claude Agent SDK**: building an agent on Claude Code's harness, permissions, sessions |
| 12 | **MCP fundamentals**: resources, tools, prompts. Build a server and use it from Claude Code |
| 13 | **Remote MCP**: Streamable HTTP, OAuth, multi-tenant concerns, the MCP connector in the API |
| 14 | **Multi-agent patterns and context management**: orchestrator/worker, evaluator loops, memory, compaction, long-running work |
| 15 | **Observability**: traces, token and cost dashboards, evals in CI, alerting. *Security track: ship agent telemetry to Splunk* |
| 16 | **Capstone 3: Fernway internal ops agent**: MCP servers for tickets, CRM and docs; an agent that drafts account health reports. *Security-track variant: a Splunk MCP server and investigation agent* |

## Phase 4 · Architecture and delivery (Weeks 17–22)

| Week | Topic |
|---|---|
| 17 | **Enterprise deployment**: Claude API vs Amazon Bedrock vs Google Vertex AI vs Microsoft Foundry; networking, identity, data retention, regions |
| 18 | **Regulated industries**: privacy, data residency, financial and health-sector rules, model risk, audit evidence. Examples drawn from Canada, the US and the EU. *Check the current status of each source when you get here* |
| 19 | **Cost, latency and capacity**: model routing, caching strategy, batching, rate limits, a cost model a finance team will accept |
| 20 | **Shipping**: a FastAPI service, Docker, CI with evals as a gate, a human-review UI |
| 21 | **Customer skills**: discovery interviews, success metrics, scoping, demos, change management, writing for executives |
| 22 | **Capstone 4: Harbourview Health policy assistant**: retrieval with access control, citations, health-data handling, an architecture decision record, a cost model |

## Phase 5 · Residency simulation (Weeks 23–24)

| Week | Topic |
|---|---|
| 23 | **Four-day intensive, simulated.** Draw an unseen scenario card. Day 1 discovery and design, days 2–3 build and evals, day 4 security review, handover and demo. Strict time box |
| 24 | **Portfolio and interview prep**: polish your capstones, write two public posts, practise interview loops (use-case screen, solution design, coding, values) |

## Pace

- Behind? Cut stretch exercises and security-track labs first, never the evals or the security reviews.
- Ahead? Run each capstone on two models and write up the cost/quality trade-off. That's exactly the analysis customers ask for.
