# Syllabus

24 weeks at roughly 12–15 hours a week. Each phase opens with a **checkpoint** you can use to skip material you already know, and closes with a capstone for a new customer.

!!! abstract "What an FDE needs, and where it's covered"
    | Skill | Weeks |
    |---|---|
    | Claude API, models, cost, latency | 1, 19 |
    | Prompting, structured outputs, caching | 2 |
    | **Evals**: proving a system works | 3, every capstone |
    | Claude Code as a delivery tool (CLAUDE.md, skills, hooks, subagents, headless) | 5 |
    | Tool use and integrations | 6, 8 |
    | Retrieval, long context, documents, citations | 7 |
    | Agent security and prompt injection | 9, every capstone |
    | Claude Agent SDK, multi-agent patterns, context management | 11, 14 |
    | MCP servers, local and remote, with auth | 12, 13 |
    | Observability and operations | 15 |
    | Enterprise deployment, cloud platforms, data residency | 17, 18 |
    | Shipping: services, containers, CI, human review UIs | 20 |
    | Discovery, scoping, demos, change management, writing | 4, 10, 16, 21, 22 |

## Phase 0 · Setup (before Week 1)

[Workstation setup](setup/index.md): Python, Git, Claude Code, an API key with a spend limit, and this repo. Optional: the [Splunk lab](setup/splunk-lab.md) for the security track.

## Phase 1 · Foundations (Weeks 1–4) ✅ written

| Week | Topic | Labs |
|---|---|---|
| 1 | [Claude API essentials](phase-1/week-01.md): messages, models, tokens, cost, streaming, errors | First call, token counting, streaming, error zoo, multi-turn cost, usage report |
| 2 | [Prompting for real work](phase-1/week-02.md): system prompts, structure, structured outputs, caching | Prompt ladder, ticket triage, caching. *Stretch: SOC alert triage* |
| 3 | [Evals](phase-1/week-03.md): golden sets, code graders, LLM-as-judge, regression gates | Eval runner, run diff, calibrated judge |
| 4 | [Capstone 1: Claims intake for Lakeshore Mutual](phase-1/week-04-capstone.md) | Discovery → extractor → rules → evals → security review → handover |

## Phase 2 · Production building blocks (Weeks 5–10)

| Week | Topic |
|---|---|
| 5 | **Claude Code as an FDE tool**: CLAUDE.md, skills, hooks, subagents, headless mode in CI. *Checkpoint: your existing guardrail-hooks project counts. Write it up as a portfolio piece.* |
| 6 | **Tool use**: tool schemas, strict tools, parallel calls, the agent loop, tool errors |
| 7 | **Documents and retrieval**: long context vs RAG, chunking, contextual retrieval, the Files API, citations |
| 8 | **Integrations**: REST APIs, webhooks, auth, idempotency, retries, Message Batches for bulk work |
| 9 | **Agent security**: prompt-injection threat modelling, least privilege, approval gates, output handling. *Security track: SOC agent red-team* |
| 10 | **Capstone 2: Northwind Outfitters support agent**: order lookup, refunds behind human approval, policy retrieval, escalation, evals and a red-team report |

## Phase 3 · Agents and MCP (Weeks 11–16)

| Week | Topic |
|---|---|
| 11 | **Claude Agent SDK**: building an agent on Claude Code's harness, permissions, sessions |
| 12 | **MCP fundamentals**: resources, tools, prompts. Build a stdio server and use it from Claude Code |
| 13 | **Remote MCP**: Streamable HTTP, OAuth, multi-tenant concerns, the MCP connector in the API |
| 14 | **Multi-agent patterns and context management**: orchestrator/worker, evaluator loops, memory, compaction, long-running work |
| 15 | **Observability**: traces, token and cost dashboards, eval-in-CI, alerting. *Ship agent telemetry to Splunk via HEC, your home turf* |
| 16 | **Capstone 3: Fernway internal ops agent**: MCP servers for tickets, CRM and docs; an agent that drafts account health reports. *Security-track variant: Splunk MCP server + investigation agent* |

## Phase 4 · Architecture and delivery (Weeks 17–22)

| Week | Topic |
|---|---|
| 17 | **Enterprise deployment**: Claude API vs Amazon Bedrock vs Google Vertex AI vs Microsoft Foundry; networking, identity, data retention, regions |
| 18 | **Regulated industries**: privacy and data residency (PIPEDA, Quebec Law 25, PHIPA), financial-sector guidance (OSFI B-10, E-23), model risk, audit evidence. *Check the current status of each when you get here* |
| 19 | **Cost, latency and capacity**: model routing, caching strategy, batching, rate limits, a cost model a CFO will accept |
| 20 | **Shipping**: a FastAPI service, Docker, CI with evals as a gate, a human-review UI |
| 21 | **Customer skills**: discovery interviews, success metrics, scoping, demos, change management, writing for executives |
| 22 | **Capstone 4: Harbourview Health policy assistant**: retrieval with access control, citations, PHI handling, an architecture decision record, a cost model |

## Phase 5 · Residency simulation (Weeks 23–24)

| Week | Topic |
|---|---|
| 23 | **Four-day intensive, simulated.** Draw an unseen scenario card. Day 1 discovery and design, days 2–3 build and evals, day 4 security review, handover and demo. Strict time box. |
| 24 | **Portfolio and interview prep**: polish four capstones, write two public posts, mock loops (use-case screen, solution design, coding, values) |

## Pace

- Behind? Cut stretch labs first, never the evals or the security review.
- Ahead? Run each capstone on two models and write up the cost/quality trade-off. That's exactly the analysis customers ask for.
