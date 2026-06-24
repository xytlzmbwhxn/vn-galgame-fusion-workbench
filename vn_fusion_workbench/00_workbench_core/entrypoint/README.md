# Workbench Web Entry

This folder contains the workbench-owned local entrypoint inspired by AI-native
novel production tools.

It intentionally does not copy the external project's React, Express, Prisma, or
prompt files. It adapts the useful structure into a lightweight local runtime:

- project and scene selector
- workflow actions
- validation and deep audit
- readable rendering and engine export
- OpenAI-compatible AI call through local route config
- generated AI responses stored under the active project's `02_generated_content/ai_assist/`

## Start

From `vn_fusion_workbench`:

```powershell
py .\00_workbench_core\entrypoint\vn_workbench_server.py --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

Or use the Chinese launcher at the workbench root:

```powershell
.\启动视觉小说工作台.ps1
```

## AI Route

The server stores non-secret model route config in:

```text
00_workbench_core/runtime/llm_routes.json
```

Secrets are read from environment variables only. Default:

```powershell
$env:OPENAI_API_KEY="..."
```

Any OpenAI-compatible endpoint can be used by changing `base_url`, `model`, and
`api_key_env` in the web UI.

