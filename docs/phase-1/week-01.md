# Week 1 · Claude API essentials

**Goal:** call Claude from code the way production systems do: logged, costed, with the failure modes handled.

*Facts checked against the Claude docs on 2026-10-06. Models and prices change, so see [Models and pricing](../reference/models.md).*

## Lesson

### The Messages API in one paragraph

You send a **model id**, a **max_tokens** ceiling, an optional **system** prompt and a list of **messages** that alternate `user` / `assistant`. You get back a list of **content blocks** (text, and later tool calls), a **stop_reason** and **usage** (token counts). The API is stateless: for a conversation you resend the whole history each turn.

```python
import anthropic

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=300,
    system="You are a senior SOC analyst. Answer in at most three sentences.",
    messages=[{"role": "user", "content": "What is a SIEM correlation search?"}],
)
print(response.content[0].text, response.stop_reason, response.usage)
```

### Choosing a model

| Model | API id | $/MTok in / out | Use it for |
|---|---|---|---|
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 1 / 5 | High-volume classification and extraction, sub-agents, latency-sensitive steps |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 2 / 10 | Most production work, the default in these labs |
| Claude Opus 5.5 | `claude-opus-5-5` | 4 / 20 | Hard reasoning, agents that plan, judges in evals |
| Claude Fable 5.1 | `claude-fable-5-1` | 10 / 50 | The most demanding long-horizon agentic work |

The FDE habit: **start with the strongest model that's affordable, get the eval passing, then try cheaper models against the same eval.** Never downgrade on vibes.

### Tokens and cost

You pay per token in and per token out, and output costs about 5× input. Things that surprise people:

- **JSON and logs tokenise badly.** Expect around 2–3 characters per token, not the 4 people quote for prose. Lab 2 measures it.
- **Conversation history is re-billed every turn.** Lab 5 shows the input growing.
- **Thinking tokens bill as output.** Adaptive thinking is on for the newest models, and the **effort** setting (`output_config={"effort": ...}`) trades thoroughness for tokens. It's supported on the Sonnet, Opus and Fable models above, not Haiku 4.5.
- **Counting tokens is free:** `client.messages.count_tokens(...)`. Use it to price a design before you build it.

### Stop reasons

Check `stop_reason` on every response:

| stop_reason | Meaning | Your code should |
|---|---|---|
| `end_turn` | Finished normally | Carry on |
| `max_tokens` | Hit your ceiling; output is **truncated** | Raise the ceiling or ask for less. Never parse a truncated answer as complete |
| `tool_use` | Wants to call a tool (Week 6) | Run the tool and continue |
| `refusal` | Declined | Log it and route to a human |
| `pause_turn`, `model_context_window_exceeded` | Long-running or oversized requests | Covered in Phase 3 |

### Sampling parameters are gone

Older tutorials (including the first draft of this course) set `temperature=0` for "deterministic" output. **Models released after Claude Opus 4.6 reject `temperature` values other than 1.0, `top_p` below 0.99, and any `top_k`, with a 400 error.** Get consistency from structure instead: clear instructions, examples, structured outputs (Week 2), and evals that measure stability (Week 3).

### Errors and retries

The SDK retries connection errors, 408, 409, 429 and 5xx with exponential backoff (2 retries by default; the labs set 3). Your job:

- **Never retry** 400, 401, 403 or 404. The request is wrong, so fix it.
- **Set timeouts.** A hung call in a batch job is worse than a failed one.
- **Log the request id** (`response._request_id`, or `e.request_id` on errors). Support asks for it.

### Streaming

`client.messages.stream(...)` returns text as it's generated. Total latency doesn't change, but time to first token drops, which is what users feel. Stream anything a human waits on.

### Observability from day one

All labs call Claude through `fde_common.llm.call()` / `.parse()`, which append one line per call to `labs/runs/usage_log.jsonl`: model, tokens, cost, latency, stop reason, request id. It **never logs prompt or response text**, because logs end up in places your data shouldn't. You'll ship this log to Splunk in Phase 3.

## Labs

Run from the repo root with the venv active. Generate the sample data first: `python labs\data\generate_events.py` (no Splunk needed).

| Lab | Run | What you learn |
|---|---|---|
| 1 | `python labs\week01\01_hello.py` | A logged call; reading usage, cost and request id |
| 2 | `python labs\week01\02_count_tokens.py` | Free token counting; pricing a workload on three models |
| 3 | `python labs\week01\03_streaming.py` | Time to first token vs total time |
| 4 | `python labs\week01\04_errors.py` | Truncation, wrong model, a rejected `temperature`, bad key, timeout |
| 5 | `python labs\week01\05_multi_turn.py` | Statelessness and growing context cost |
| 6 | `python labs\week01\06_usage_report.py` | Summarise your own spend |

??? example "Lab 1 source"
    ```python
    --8<-- "labs/week01/01_hello.py"
    ```

### Exercises

1. In Lab 2, raise `--lines` to 2000. At 10,000 calls a day, what does the monthly bill come to on each model? Write one sentence recommending a model to a customer, with the number.
2. Change Lab 2 to send only `user`, `src`, `action` and `app` instead of the full event. How many tokens does that save? (Trimming input is the cheapest optimisation there is.)
3. In Lab 4, which of the five cases would the SDK have retried on its own? Check against the [errors page](https://platform.claude.com/docs/en/api/errors).
4. Add `output_config={"effort": "low"}` to Lab 3 (it uses the Sonnet model). Compare output tokens and quality with the default.

## Checkpoint

- [ ] You can explain each column of `06_usage_report.py`
- [ ] You know your cost per call for Labs 1 and 2 on two models
- [ ] Your code checks `stop_reason`

## Read

- [Models overview](https://platform.claude.com/docs/en/models/overview) · [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming) · [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) · [Errors](https://platform.claude.com/docs/en/api/errors) · [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
