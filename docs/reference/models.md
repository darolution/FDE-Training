# Models and pricing

*Checked 2026-10-06 against the [models overview](https://platform.claude.com/docs/en/models/overview), [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and [effort](https://platform.claude.com/docs/en/build-with-claude/effort) docs. Re-check before quoting a number to anyone.*

| Model | API id | Input $/MTok | Output $/MTok | Context | Max output | Effort param |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 10 | 50 | 1M | 128K | Yes |
| Claude Opus 5.5 | `claude-opus-5-5` | 4 | 20 | 1M | 128K | Yes (default `medium`) |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 2 | 10 | 1M | 128K | Yes (default `high`) |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 1 | 5 | 200K | 64K | No |

## Prompt caching

| | Multiplier on input price |
|---|---|
| Cache write, 5-minute TTL | 1.25× |
| Cache write, 1-hour TTL | 2× |
| Cache read | 0.1× (0.05× on Opus 5.5; 0.025× on Fable 5.1) |

Minimum cacheable prefix: 512 tokens on Opus 5.5 and Sonnet 5.5; 4,096 on Haiku 4.5.

## Parameters to stop using

Since Claude Opus 4.6, models reject `temperature` other than 1.0, `top_p` below 0.99, and any `top_k` (400 error). Use clear instructions, examples, structured outputs and the `effort` setting instead.

## Where these numbers live in code

`labs/fde_common/costs.py` holds the price table used by every lab. If you add a model, add its price there; the tests fail on unknown models on purpose.
