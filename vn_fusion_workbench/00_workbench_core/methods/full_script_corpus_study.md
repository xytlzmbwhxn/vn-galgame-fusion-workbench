# Full Script Corpus Study

## Purpose

Use legally available complete VN/Ren'Py scripts as a measurable reference layer.
The workbench studies full source files for structure, pacing, production cues,
choice architecture, and system coupling without copying prose or dialogue.

## When To Load

Load this method when the user asks to reference actual complete works, mature
VN scripts, open-source VN projects, or when a new script sample must prove it
is grounded in real project structure rather than one-off advice.

## Inputs

- `01_reference_log/full_script_corpus/corpus_manifest.json`
- `01_reference_log/full_script_corpus/full_script_metrics.json`
- `01_reference_log/full_script_corpus/LEGAL_FULL_SCRIPT_CORPUS.md`
- Selected scene/project memory for the new original work.

## Procedure

1. Run the corpus analyzer before drafting or expanding a serious VN sample.
2. Pick one primary corpus for flow shape and one secondary corpus for mechanic
   structure. Do not pick a corpus for wording imitation.
3. Record target metrics in the draft session:
   - expected textbox length band
   - dialogue/narration balance
   - choice/menu density
   - staging cue density
   - system-state density
4. Translate corpus lessons into original scene constraints:
   - master flow vs scene file split
   - visible production cues
   - route/choice/state bookkeeping
   - replay-safe consequences
   - no copied names, prose, jokes, CG wording, or signature set pieces
5. After drafting, compare the produced CSV with the selected metric targets.

## Output Contract

Before claiming a script references complete VN texts, the workbench must show:

- which legal complete scripts were analyzed
- commit/local path/license note
- aggregate metrics, not copied source text
- the structural lesson being reused
- the original pressure that replaces the reference premise
- which local QA rule will catch drift

## Hard Stops

- Do not paste full commercial scripts into the workbench.
- Do not rewrite a copyrighted scene with renamed characters.
- Do not store source dialogue or narration as examples.
- Do not use metrics as a template. If the original story needs a different
  rhythm, state why and make the exception visible in the draft session.

## Reusable Command

```powershell
py .\00_workbench_core\tools\analyze_full_script_corpus.py --manifest .\01_reference_log\full_script_corpus\corpus_manifest.json --out-dir .\01_reference_log\full_script_corpus
```
