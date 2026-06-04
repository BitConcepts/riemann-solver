# Session Protocol

See AGENTS.md for the full specsmith Session Governance Protocol.

## Session start

```bash
specsmith kill-session 2>/dev/null || true
specsmith audit --project-dir .
specsmith sync --project-dir .
specsmith checkpoint --project-dir .
```

Output the checkpoint block verbatim as first response.

## Before every code change

```bash
specsmith preflight "<describe the change>" --json
```

- `accepted` → proceed with `work_item_id`
- `needs_clarification` → surface instruction first
- Never make a code change without an accepted preflight.

## Session end

```bash
specsmith save --project-dir .
specsmith kill-session
```

Never end a session with uncommitted governance changes.
