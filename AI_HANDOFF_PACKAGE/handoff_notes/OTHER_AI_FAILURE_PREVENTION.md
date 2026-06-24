# OTHER_AI_FAILURE_PREVENTION

This file exists because previous assistants failed in repeatable ways. Treat these as hard operational warnings.

## Do Not Leak

User-facing drafts and final answers must not contain:

- hidden chain markers;
- internal context package names;
- tool scratch notes;
- broken encoding replacement characters;
- unexplained English control text inside Chinese creative deliverables.

Tool output may be English, but final explanations and creative drafts should follow the user's requested language.

## Handoff Path Rule

Correct:

```text
VN_Workbench_Project/AI_HANDOFF_PACKAGE
```

Wrong:

```text
VN_Workbench_Project/vn_fusion_workbench/AI_HANDOFF_PACKAGE
```

## Search Rule

Do not run `rg` over the whole workbench root without exclusions. It may include dependency folders, runtime receipts, generated packages and large internal work areas.

Prefer targeted searches or exclude:

```powershell
rg <pattern> . --glob '!node_modules/**' --glob '!**/99_内部工作/**'
```

## GitHub Rule

Before upload:

```powershell
git status --ignored
git status --short
```

Important public files must remain visible:

- `README.md`
- `START_HERE.md`
- `GITHUB_UPLOAD_GUIDE.md`
- `skills/`
- `AI_HANDOFF_PACKAGE/portable_skills/`
- `vn_fusion_workbench/00_workbench_core/tools/`
- `vn_fusion_workbench/00_workbench_core/methods/`
- `vn_fusion_workbench/06_学习输入/_风格画像/`

## Delivery Rule

Never claim a VN project is complete if it only has a readable Markdown draft. A complete delivery package must include:

- readable MD;
- source CSV;
- public CSV;
- Excel;
- WebGAL / Ren'Py / Ink / Yarn / Godot Dialogue exports;
- character card package;
- character brief;
- QA reports;
- runtime states;
- memory logs;
- route map;
- state delta when the scene changes canon.

Use:

```powershell
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project <Pxxx> --strict
```

## Writing Failure Rule

Do not start a new work by assuming the user already knows all characters. The opening should usually begin with a problem, environment, object, question, pressure, or small action that invites the player into the scene.

Do not flatten interiority into rigid statements. Thought can contain hesitation, breath, small retreat, self-mockery, soft particles, and character-owned uncertainty when the moment calls for it.
