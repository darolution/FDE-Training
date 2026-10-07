# Phase 3 · Agents and MCP

**Weeks 11–16 · not yet written.**

**Capstone 3: Fernway internal ops agent.** Fernway (fictional) is a company that sells software to other businesses. Build MCP servers for its ticketing system, CRM and docs (mock services provided), and an agent built on the Claude Agent SDK that drafts weekly account-health reports for customer success managers. Its traces and costs feed a monitoring dashboard. *Security-track variant: a Splunk MCP server and an investigation agent graded against the planted incidents.*

| Week | Topic | Key outcomes |
|---|---|---|
| 11 | Claude Agent SDK | An agent with custom tools, permission modes, sessions; when to use the SDK and when to write your own loop |
| 12 | MCP fundamentals | Build a stdio MCP server (resources, tools, prompts) and use it from Claude Code |
| 13 | Remote MCP | Streamable HTTP transport, OAuth, tenant isolation, the MCP connector in the Messages API |
| 14 | Multi-agent patterns and context | Orchestrator/worker, evaluator-optimizer, memory, compaction, long-running tasks |
| 15 | Observability | Structured traces, cost and latency dashboards, evals in CI as a merge gate. *Security track: the same telemetry in Splunk via HEC* |
| 16 | Capstone 3 | Discovery → build → evals → security review → handover |

Read ahead: [MCP](https://modelcontextprotocol.io/) · [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) · [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) · [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
