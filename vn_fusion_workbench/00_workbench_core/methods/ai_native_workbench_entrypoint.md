---
id: ai_native_workbench_entrypoint
type: method_card
---

# AI Native Workbench Entrypoint

## Call This When

When the user wants the VN workbench to stop being only a chat-mediated folder and
gain its own operation surface.

## Source Adaptation

Inspired by external AI writing assistant product patterns:

- Creative Hub as a unified operation surface
- model routing
- workflow actions with visible status
- style assets and anti-AI rules
- task center / recoverable execution thinking

This workbench adapts the pattern without copying the external app's original code.

## Local Rule

The VN workbench must have a first-class entrypoint:

```text
00_workbench_core/entrypoint/vn_workbench_server.py
00_workbench_core/tools/vn_control_room.py
```

The entrypoint should expose the most common pipeline actions:

- list projects, scenes, scripts
- show file-based project status and one recommended next step
- create command-ledger entries before running controlled actions
- create draft-session
- validate
- deep-audit
- render readable draft
- export engine scripts
- render character brief
- compile style contract
- classify VN quality debt
- call an OpenAI-compatible model using local context

## AI Invocation Boundary

AI calls must assemble local context from draft-session, scene brief, context pack,
method cards, character cards, runtime state, and project memory.

Secrets must not be saved in the project. The route config stores only:

- provider
- base_url
- model
- api_key_env
- temperature

The actual key comes from environment variables.

## Output Contract

AI-generated raw responses go under:

```text
02_projects/<project_id>/02_generated_content/ai_assist/
```

They are not canon until converted into CSV and passed through `validate` and
`deep-audit`.

## Control Plane Rule

The local web UI should use `vn_control_room.py` for controlled workbench actions.
`vn_control_room.py` writes command records under:

```text
00_workbench_core/runtime/commands/command_ledger.jsonl
```

This makes the workflow inspectable by another AI and prevents one-off chat actions
from becoming invisible production state.
