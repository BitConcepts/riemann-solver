# Agent Lifecycle

## AEE Phase

Current phase: **Verification**. See `specsmith checkpoint` for live status.

Phase sequence: inception → architecture → requirements → test_spec → implementation → verification → release

## Work items

Track active work items via `specsmith status`. All code changes require an accepted
`specsmith preflight` before execution.

## Commit discipline

Every commit must include `Co-Authored-By: Oz <oz-agent@warp.dev>` when agent-generated.

## Drift recovery

If context feels compressed or any governance state is unknown:
```bash
specsmith checkpoint --project-dir .
```
Output the GOVERNANCE ANCHOR verbatim, then re-anchor.
