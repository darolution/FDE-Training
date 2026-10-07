# Week 2 · Prompting for real work

**Goal:** turn messy customer input into reliable, schema-valid output. **Dataset:** 24 synthetic support tickets for *Northwind Outfitters*, a fictional Canadian outdoor-gear retailer. They're in English and French, and include two prompt-injection attempts, a safety incident and a legal threat (`labs/data/tickets_golden.jsonl`).

## Lesson

### A system prompt is a spec

The prompt in `labs/week02/prompts/ticket_triage_system.md` is structured the way a good spec is:

| Section | Why it's there |
|---|---|
| Who and what (role, company, who reads the output) | Sets vocabulary and judgment |
| `<categories>` with a definition for **every** label | The model can't guess your taxonomy, and neither can a new hire |
| `<priority_rules>`, `<needs_human_rules>` | Business rules stated explicitly, with thresholds ($200) |
| `<security>` | The input is untrusted. Flag instructions in it; never obey them |
| `<output_notes>` | Formats (order id pattern, language codes) |

XML-style tags aren't magic. They make boundaries unambiguous, both for the model and for the next engineer who edits the prompt.

### Data inside tags, instructions outside

`render_ticket()` wraps the customer text in `<ticket>...</ticket>` after **redacting** obvious secrets and identifiers (`fde_common/redact.py`). The system prompt says that everything inside the tags is data. This doesn't make injection impossible, so later weeks add more layers, but it's the baseline every deployment needs.

### Structured outputs

Asking for JSON in the prompt works most of the time. **Structured outputs** make it work every time: pass a schema and the response is constrained to match it.

```python
from pydantic import BaseModel

class TicketTriage(BaseModel):
    category: Category          # an Enum, so only valid labels are possible
    priority: Priority
    needs_human: bool
    ...

response = client.messages.parse(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system=system_prompt,
    messages=[{"role": "user", "content": "<ticket>...</ticket>"}],
    output_format=TicketTriage,
)
result = response.parsed_output    # a TicketTriage instance
```

Two things to remember:

1. **Valid isn't correct.** The schema guarantees shape, not truth. That's what Week 3's evals are for.
2. **Enums are your friend.** A free-text "category" field drifts ("Shipping", "shipping issue", "Delivery"…). An enum can't.

Structured outputs are supported on Haiku 4.5, Sonnet 4.5 and later, Opus 4.5 and later, and Fable 5.x. Without the SDK helper, the raw form is `output_config={"format": {"type": "json_schema", "schema": {...}}}`.

### Examples (few-shot)

One or two worked examples inside `<examples>` teach format and judgment faster than paragraphs of rules. Pick examples that show the hard calls (a borderline priority, a benign message that looks alarming), not the easy ones. See the SOC prompt in `labs/week02/prompts/soc_triage_system.md` for the pattern.

### Prompt caching

If every request starts with the same long prefix (a system prompt, policy text, tool definitions), cache it:

- Mark the end of the stable prefix with `cache_control: {"type": "ephemeral"}` (`tickets.triage(..., cache=True)` does this on the system block).
- The first call **writes** the cache at 1.25× the input price (5-minute TTL; 2× for the 1-hour TTL). Calls within the TTL **read** it at 0.1× (0.05× on Opus 5.5).
- Minimum cacheable prefix: **512 tokens** on Sonnet 5.5 and Opus 5.5, **4,096** on Haiku 4.5. Shorter prefixes silently don't cache.
- Order matters: stable content first, variable content last.

Check `usage.cache_creation_input_tokens` and `usage.cache_read_input_tokens` to confirm it's working. `fde_common.costs.cost_usd()` prices both.

## Labs

| Lab | Run | What you learn |
|---|---|---|
| 1 | `python labs\week02\01_prompt_ladder.py` | Three prompts, same schema, eight tickets: watch which fields improve as instructions get specific |
| 2 | `python labs\week02\02_structured_triage.py --model fast` | Triage all 24 tickets; results saved for Week 3's judge |
| 3 | `python labs\week02\03_prompt_caching.py` | Cache write vs read, and the saving in dollars |
| Stretch | `python labs\week02\04_stretch_soc_triage.py` | **Security track:** triage alerts built from the synthetic SIEM data, including one with injection text in a user-agent |

### Exercises

1. In the ladder, prompt **B** usually misses `needs_human` and injection. Add *one* sentence to B that fixes the injection flag without adding the full rules. What did you learn about which instructions carry the most weight?
2. T-024 tries to change its own category. Does your model obey any part of it? Read its summary closely.
3. Add a new category, `warranty`, to the enum and prompt. Which existing tickets move? Is that what the business would want? (This is a scope conversation, not a prompt tweak.)
4. Run Lab 2 with `--model default` and compare five tickets side by side. Don't judge which is "better" yet; Week 3 gives you the tools.

## Checkpoint

- [ ] You can explain each section of the triage prompt and what breaks if it's removed
- [ ] You've seen a cache read in the usage fields
- [ ] You can say why structured outputs don't make the triage correct

## Read

- [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
