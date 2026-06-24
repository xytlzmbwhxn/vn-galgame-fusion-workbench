---
id: workflow_runtime_status
type: method_card
---

# Workflow Runtime Status

## Call This When

When building a local entrypoint, automating multiple workbench steps, or showing
the user what the workbench can do next.

## Rule

A creative workflow is not a single prompt. It is a sequence of observable steps:

- prepare context
- draft or import script
- validate
- deep-audit
- repair
- export
- archive human-facing output

Each step should have:

- input artifact
- output artifact
- status
- command or AI call used
- next recommended action

## First MVP Surface

The workbench entrypoint may start as a lightweight local web UI backed by the
existing Python tool. It does not need a database at first, but it must make the
pipeline visible and repeatable.

## Canon Rule

Generated text is draft material until the workflow status says:

- CSV source exists
- `validate` passed
- `deep-audit` passed
- readable preview exists
- exports or Excel were generated when requested

