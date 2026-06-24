---
id: passage_tag_route_map
type: method_card
---

# Passage Tag Route Map

## Call This When

Before planning branching routes, optional scenes, storylets, investigation nodes, or exports to Twine/Yarn/Ink-like formats.

## Borrowed Structure

- TwineJS: passages carry names, links, tags, and story-format export behavior.
- Yarn Spinner: dialogue nodes and options remain readable while still mapping to runtime.
- ink: knots, stitches, choices, and diverts create compact narrative flow.

## Rule

Treat every scene or branch as a tagged passage, even when the immediate output is CSV.

## Tag Taxonomy

Use short tags that help retrieval and route logic:

| Tag prefix | Example | Meaning |
| --- | --- | --- |
| `route:` | `route:common` | route or branch family |
| `char:` | `char:tangmi` | character centered in the node |
| `state:` | `state:borrow_card_dirty` | state created or required |
| `lock:` | `lock:trust_2` | gate condition |
| `object:` | `object:jacket_48` | recurring prop |
| `callback:` | `callback:signature_blank` | later line or scene should echo this |
| `tone:` | `tone:comic_pressure` | performance texture |

## Procedure

1. Put route and object tags in scene cards.
2. Put state and callback tags in state delta files.
3. Put branch labels in CSV and exports.
4. Keep tag spelling stable across scene card, CSV `memory_refs`, route map, and QA notes.
5. When a tag appears three or more times, promote it into a named thread or quality.

## Output Contract

A branchable project must expose:

- passage/node ids
- route tags
- centered characters
- required state
- state created
- callback hooks
- export mapping

## Failure Signs

- optional scenes cannot be retrieved by character or object
- route locks live only in prose notes
- the same state is named three different ways
- branches are playable but not searchable by future tools
