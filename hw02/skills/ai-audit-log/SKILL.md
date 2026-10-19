---
name: ai-audit-log
description: Save verbatim user prompts and final AI responses with timestamps for an AI Audit Report. Use when a user enables persistent conversation logging or workspace instructions require logging every turn, including follow-up questions and corrections.
---

# AI Audit Log

Keep a truthful, local record of each user interaction. Use this skill on every turn while the user's logging request or workspace rule is active; do not require a repeated skill mention.

## Scope and storage

- Use the workspace root named in the applicable AGENTS.md, otherwise the user's requested folder or current workspace root. Keep that root stable when changing directories.
- Save to `ai-audit/interactions.jsonl` (append-only source) and `ai-audit/AI_Audit_Log.md` (readable report). The helper resolves all paths from `--workspace`, not its installation directory.
- Capture the user's own message exactly, including spelling, line breaks, and code. Do not log injected environment messages, system/developer instructions, hidden reasoning, or raw tool traffic as user prompts. Reference attachments by their supplied names/paths without pretending their bytes are text.
- Log the tool as `Codex (OpenAI)` in this environment. Add a model only if its identity is actually available; do not guess.
- Record capture times in UTC+07:00 for this HW2 workspace. Capture time is not the original message's sent time. For historical backfill, explicitly mark the entry as backfilled and keep unknown original times unknown.

## Every turn

1. As early as possible, write the exact user prompt to a UTF-8 temporary file under the workspace. Execute the bundled helper's `begin` command and retain its returned ID. This stores the prompt before substantive work, with status `pending`. Include each new user steering message received during work as a separate entry. Do not invent a response for an interrupted message.
2. Perform the user's task. Draft the exact final response in a UTF-8 temporary file. Before sending it, run `finish` for the matching ID with that file. Then send the same response text; if it changes after saving, do not silently claim the saved text matches.
3. Verify successful helper output before saying the interaction was saved. A failed write must be reported briefly; it must not prevent otherwise useful work. Leave interrupted or unfinished turns pending. Retry with the same ID to avoid duplicates.

The recorded AI output is the final user-facing answer. Progress commentary and tool outputs are not included automatically; retain/export the original conversation separately if those are needed as additional evidence. If several user messages share one final answer, finish each with the actual shared answer and a note explaining that relationship.

Never fabricate prior conversation text, timestamps, test results, or human review. If earlier turns are unavailable, disclose the gap. These instructions depend on the agent following them; they are not an application hook and cannot capture other apps or turns that never execute tools.

## Helper

Use an available Python 3 interpreter; no third-party packages are needed. Resolve `scripts/audit_log.py` relative to this SKILL.md. Use file-writing tools for message content rather than interpolating user text into shell commands.

```text
python <skill-dir>/scripts/audit_log.py --workspace <absolute-workspace> begin --prompt-file <utf8-file> --tool "Codex (OpenAI)" --session <stable-chat-label> [--id <unique-turn-id>] [--note <context>]
python <skill-dir>/scripts/audit_log.py --workspace <absolute-workspace> finish --id <returned-id> --response-file <utf8-file>
python <skill-dir>/scripts/audit_log.py --workspace <absolute-workspace> render
```

The helper returns JSON with the entry ID and report path. `begin` and `finish` are idempotent when retried with the same ID and content; conflicting reuse is rejected. After a crash that leaves `ai-audit/.write.lock`, inspect whether any writer is still running before removing that lock and retrying. `render` rebuilds the report from the source log without adding an interaction.
