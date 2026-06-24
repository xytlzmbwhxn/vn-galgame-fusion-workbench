# Web Entrypoint Quarantined

Date: 2026-06-22

The local web UI is quarantined. It was useful as a button surface for existing
files, but it did not support the real creative loop the user needs:

- natural-language creative direction
- repeated critique and style correction
- character setup visible to the user
- project memory creation
- scene card creation
- original script drafting
- revision based on dialogue-level criticism
- QA and export

The old server file has been moved to:

```text
00_workbench_core/experimental/web_entrypoint/vn_workbench_server.py
```

Do not treat it as the active workbench entrypoint.

Active entrypoint:

```text
Codex chat + CODEX_CHAT_CREATION_WORKFLOW.md + vn_workbench.py
```

The user talks to Codex. Codex must create or update local files, run
draft-session, write CSV/readable scripts, validate, deep-audit, and report touched
files. The web UI can be redesigned later after the chat-first workflow is proven.
