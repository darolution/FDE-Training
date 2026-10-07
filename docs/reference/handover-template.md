# Handover template

Copy this into `docs/notes/` for each capstone. A handover is good when the customer's team can run, measure and change the system **without you**.

```markdown
# <System name>: handover

**Customer:** <name>   **Date:** <YYYY-MM-DD>   **Version / commit:** <sha>

## 1. What it does (and doesn't)
- Purpose in one sentence.
- In scope: …
- Explicitly out of scope: …

## 2. Results against acceptance criteria
| Criterion | Target | Result | Evidence |
|---|---|---|---|
| … | … | … | link to eval run |

Known failure modes, with examples: …

## 3. Architecture
Diagram (Mermaid) and a short description of each component and data flow.
Which model, why, and what it costs per unit of work and per month at expected volume.

## 4. Running it
- Prerequisites and configuration (env vars, keys, where secrets live)
- How to run, how to re-run a failed batch
- Logs and audit: what's recorded, where, and for how long

## 5. Changing it safely
- Where the prompt lives; how to run the eval; what the gate is
- How to add golden cases when a new failure is reported
- Who approves rule changes (business owner)

## 6. Security and privacy
Summary of the security review: data flows, injection testing, residual risks, mitigations.

## 7. Operations
- Monitoring: what to watch (cost per day, error rate, critical-miss reports)
- Incident response: what to do if it misroutes something serious
- Model updates: how to evaluate a new model version before switching

## 8. Open items and recommendations
Prioritised next steps, each with an owner.
```
