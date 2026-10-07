# Week 1 · Claude API essentials

**Goal:** call Claude from code the way production systems do: logged, costed, and with failures handled.

**Before you start:** finish the [setup](../setup/index.md) including step 4 (API key). Activate your virtual environment and run every command from the course folder.

*Facts checked against the Claude docs on 2026-10-06. Models and prices change, so see [Models and pricing](../reference/models.md).*

??? info "New to APIs? Read this primer first (5 minutes)"
    - **Claude** is a family of AI models made by Anthropic. You can chat with it at claude.ai, but FDEs build *systems* that call it from code.
    - The **Claude API** is the door your code uses: your program sends a request over the internet and gets a response back. You covered how web APIs work in [Launchpad L6](../launchpad/l6-apis.md).
    - The **SDK** is the `anthropic` Python package. It turns API calls into ordinary Python function calls.
    - Your **API key** proves the request comes from your account, which is billed for it.
    - Models read and write text in **tokens**, small chunks of a word. You pay per token.

    That's all you need to start. Every other term is in the [glossary](../glossary.md).

## Lesson

### The Messages API in one paragraph

You send a **model id**, a **max_tokens** ceiling, an optional **system** prompt and a list of **messages** that alternate `user` and `assistant`. You get back a list of **content blocks** (text, and later tool calls), a **stop_reason** and **usage** (token counts). The API is stateless: for a conversation, you resend the whole history every turn.

```python
import anthropic

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY from the environment
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=300,
    system="You are an experienced customer-support team lead. Answer in at most three sentences.",
    messages=[{"role": "user", "content": "What is a service-level agreement for support tickets?"}],
)
print(response.content[0].text)   # the answer
print(response.stop_reason)       # why it stopped
print(response.usage)             # tokens in and out
```

### Choosing a model

| Model | API id | $ per million tokens, in / out | Use it for |
|---|---|---|---|
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 1 / 5 | High-volume classification and extraction, fast sub-steps |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 2 / 10 | Most production work; the default in these labs |
| Claude Opus 5.5 | `claude-opus-5-5` | 4 / 20 | Hard reasoning, agents that plan, judges in evals |
| Claude Fable 5.1 | `claude-fable-5-1` | 10 / 50 | The most demanding long-running agent work |

The FDE habit: **start with the strongest model you can afford, get the eval passing (Week 3), then try cheaper models against the same eval.** Never downgrade on gut feel.

### Tokens and cost

You pay per token in and per token out, and output costs about 5× as much as input. Things that surprise people:

- **JSON and non-English text use more tokens** per character than plain English. Lab 2 measures it.
- **Conversation history is re-billed every turn.** Lab 5 shows the input growing.
- **Thinking tokens bill as output.** The newest models think adaptively, and the **effort** setting (`output_config={"effort": ...}`) trades thoroughness for tokens. It works on the Sonnet, Opus and Fable models above, not Haiku 4.5.
- **Counting tokens is free:** `client.messages.count_tokens(...)`. Use it to price a design before you build it.

### Stop reasons

Check `stop_reason` on every response:

| stop_reason | Meaning | Your code should |
|---|---|---|
| `end_turn` | Finished normally | Carry on |
| `max_tokens` | Hit your ceiling, so the output is **cut off** | Raise the ceiling or ask for less. Never treat a cut-off answer as complete |
| `tool_use` | Wants to call a tool (Week 6) | Run the tool and continue |
| `refusal` | Declined to answer | Log it and route to a human |
| `pause_turn`, `model_context_window_exceeded` | Long-running or oversized requests | Covered in Phase 3 |

### Settings that no longer exist

Older tutorials set `temperature=0` to get "the same answer every time". **Models released after Claude Opus 4.6 reject `temperature` values other than 1.0, `top_p` below 0.99, and any `top_k`, with a 400 error.** Get consistency from structure instead: clear instructions, examples, structured outputs (Week 2), and evals that measure stability (Week 3).

### Errors and retries

The SDK automatically retries network errors and responses 408, 409, 429 and 5xx, waiting a little longer each time (2 retries by default; the labs use 3). Your job:

- **Never retry** 400, 401, 403 or 404. The request itself is wrong, so fix it.
- **Set timeouts.** A hung call in a batch job is worse than a failed one.
- **Log the request id** (`response._request_id`, or `e.request_id` on errors). Support will ask for it.

### Streaming

`client.messages.stream(...)` returns text as it's generated. The total time is the same, but the first words arrive much sooner, and that's what users notice. Stream anything a person is waiting for.

### Logging from day one

All labs call Claude through `fde_common.llm.call()` or `.parse()`. Each call adds one line to `labs/runs/usage_log.jsonl` with the model, tokens, cost, time taken, stop reason and request id. It **never logs the prompt or the answer**, because logs end up in places your data shouldn't. You'll build dashboards from this log in Phase 3.

## Labs

| Lab | Run | What you learn |
|---|---|---|
| 1 | `python labs/week01/01_hello.py` | A logged call; reading usage, cost and request id |
| 2 | `python labs/week01/02_count_tokens.py` | Free token counting; pricing a workload on three models |
| 3 | `python labs/week01/03_streaming.py` | Time to first token vs total time |
| 4 | `python labs/week01/04_errors.py` | Cut-off output, wrong model id, a rejected `temperature`, bad key, timeout |
| 5 | `python labs/week01/05_multi_turn.py` | Statelessness and growing context cost |
| 6 | `python labs/week01/06_usage_report.py` | Summarise your own spend |

??? example "Lab 1 source code"
    ```python
    --8<-- "labs/week01/01_hello.py"
    ```

??? success "What Lab 1 output looks like"
    Your wording, numbers and request id will differ:
    ```text
    An SLA for support tickets is a promise about how quickly the team will respond to and resolve...
    ------------------------------------------------------------
    model:        claude-haiku-4-5-20251001
    stop_reason:  end_turn
    tokens:       in=45 out=78
    cost:         $0.000435
    request id:   req_011C...
    logged to:    .../labs/runs/usage_log.jsonl
    ```

??? failure "If something goes wrong"
    | You see | Fix |
    |---|---|
    | `ConfigError: ANTHROPIC_API_KEY is not set` | Create `labs/.env` from `labs/.env.example` and paste your key (setup step 4) |
    | `ModuleNotFoundError: No module named 'anthropic'` | Your virtual environment isn't active. Activate it and try again |
    | `AuthenticationError` | The key is wrong or revoked. Create a new one in the Console |
    | A credit or billing error, or a spend-limit error | Add credit or raise the limit in the Console (see [Costs](../costs.md)) |
    | `RateLimitError` after retries | Wait a minute and run again |

### Exercises

1. **Core.** Run Lab 2, then again with `--copies 50`. At 10,000 calls a day, what would a month cost on each model? Write one sentence recommending a model to a customer, with the number.
2. **Core.** In Lab 4, which of the five cases would the SDK have retried on its own? Check against the [errors page](https://platform.claude.com/docs/en/api/errors).
3. **Core.** Change the question in Lab 1 to something from a job you know. Run it on the `fast` and `default` models (edit `m.fast` to `m.default`) and compare the answers and the cost.
4. **Stretch.** Add `output_config={"effort": "low"}` to the `stream(...)` call in Lab 3 (it uses the Sonnet model). Compare the output tokens and the quality with the default.

## Checkpoint

- [ ] You can explain each column of `06_usage_report.py`
- [ ] You know your cost per call for Labs 1 and 2 on two models
- [ ] You know why code must check `stop_reason`

## Read

- [Models overview](https://platform.claude.com/docs/en/models/overview) · [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming) · [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) · [Errors](https://platform.claude.com/docs/en/api/errors) · [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- Free courses: [Anthropic Academy](https://academy.claude.com/)
