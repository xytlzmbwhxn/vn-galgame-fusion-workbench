# Path Alias Protocol

This file exists to stop PowerShell + Chinese-path friction from wasting time.

## Core Rule

When using shell commands, do not hand-write Chinese subpaths inside inline
PowerShell or Python snippets.

Use one of these instead:

1. ASCII-safe project keys such as `P017`
2. ASCII-safe path aliases such as `LEARN_VN_DONE`
3. `vn_workbench.py read` for UTF-8 file reading
4. `vn_workbench.py paths resolve` for path lookup
5. ASCII-root scanning plus glob filters when a concrete Chinese filename is needed

## Project Keys

Projects under `02_projects/` are auto-resolved by numeric prefix:

- `P001`
- `P017`

Example:

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths projects
py .\00_workbench_core\tools\vn_workbench.py paths scenes --project P017
py .\00_workbench_core\tools\vn_workbench.py paths scripts --project P017
```

## Path Aliases

List all aliases:

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths list
```

Resolve one alias:

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths resolve LEARN_VN_DONE
py .\00_workbench_core\tools\vn_workbench.py paths resolve STYLE_ASSETS
py .\00_workbench_core\tools\vn_workbench.py paths resolve STYLE_HANDPRINT_CURRENT
py .\00_workbench_core\tools\vn_workbench.py paths resolve STYLE_HANDPRINT_CURRENT
py .\00_workbench_core\tools\vn_workbench.py paths resolve P017 --kind project
```

## UTF-8 Reading

Do not prefer raw `Get-Content` for Chinese files during AI work.

Use:

```powershell
py .\00_workbench_core\tools\vn_workbench.py read ROOT_START_HERE
py .\00_workbench_core\tools\vn_workbench.py read PATH_ALIAS_PROTOCOL.md
py .\00_workbench_core\tools\vn_workbench.py read chinese_vn_generation_hard_gates.md
py .\00_workbench_core\tools\vn_workbench.py read S001_scene_card.json --kind scene --project P017
```

Generic `read` searches the workbench root plus core `docs/`, `methods/`,
`references/`, `portable_skills/`, and style-profile folders by filename. If a
name is ambiguous, use an alias or `--kind scene/script --project Pxxx`.

## Writing / QA Commands Without Chinese Paths

Draft session:

```powershell
py .\00_workbench_core\tools\vn_workbench.py draft-session --project P017 --scene S001_scene_card.json --draft-name S001_demo
```

Validate CSV by filename inside the project's canonical CSV folder:

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project P017 --script S001_demo.csv
```

Deep audit:

```powershell
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project P017 --script S001_demo.csv
```

## Why This Exists

The failure mode is not only output mojibake. The bigger problem is that inline
PowerShell / Python commands sometimes receive Chinese path literals as question-mark placeholders,
which breaks file resolution and wastes tokens. Project keys and aliases avoid
that entire class of failure.

## Encoding Guard

Before final delivery, and after any tool-generated CSV / Markdown / JSON file,
run the encoding guard from the workbench root:

```powershell
py .\00_workbench_core\tools\vn_encoding_guard.py --project P017
```

For the whole formal workbench:

```powershell
py .\00_workbench_core\tools\vn_encoding_guard.py
```

The guard intentionally ignores normal URL query marks. It only reports real
mojibake markers, replacement characters, and structured placeholder fields such
as `speaker=??`.

If a command needs to inspect a Chinese-named file, write the command with an
ASCII root and locate the file by project key, numeric prefix, alias, or glob.
Do not paste the Chinese path into inline Python or PowerShell source.
