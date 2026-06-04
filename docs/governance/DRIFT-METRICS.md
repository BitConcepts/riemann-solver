# Drift Metrics

## Drift detection questions

If you cannot answer these from memory, you have drifted — run `specsmith checkpoint` immediately:

- What is the current AEE phase?
- What work item is active?
- What was the last preflight decision?
- Is the audit currently healthy?
- What is the current bridge research status (H13)?

## Mathematical drift indicators

- Any claim of "RH proved" without H13 being established → **IMMEDIATE HALT**
- Any source citation without primary-text verification → flag as SOURCE-CLAIM, not PROVED
- Any computation promoted to PROVED without IA certificate → **REJECT**

## Recovery

```bash
specsmith checkpoint --project-dir .
cat phase-next/reports/bridge_status_matrix.md
cat phase-next/research_log.md | tail -50
```
