# Context Budget

## Governance heartbeat

Run every 8–10 turns (or when context feels compressed):

```bash
specsmith checkpoint --project-dir .
```

Output the GOVERNANCE ANCHOR block verbatim.

## Context summary protocol

1. Run `specsmith checkpoint` first.
2. Place GOVERNANCE ANCHOR at the **top** of the summary.
3. Never omit phase, work items, or health status from a summary.

## Modular governance files

Large governance content is split across `docs/governance/`:
- `RULES.md` — project-specific agent rules
- `SESSION-PROTOCOL.md` — session start/end commands
- `LIFECYCLE.md` — AEE phases and work items
- `ROLES.md` — human vs agent authority
- `CONTEXT-BUDGET.md` — this file
- `VERIFICATION.md` — mathematical verification standards
- `DRIFT-METRICS.md` — drift detection criteria
