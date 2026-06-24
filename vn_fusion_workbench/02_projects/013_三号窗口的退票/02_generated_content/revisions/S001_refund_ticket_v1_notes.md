# S001_refund_ticket_v1 Revision Notes

## Loaded Method Contracts
- Galgame textbox production: every row is a playable beat with stage cue density.
- Dialogue display and interiority: readable draft renders dialogue and thought separately.
- Voice state memory: all three speakers have character cards and runtime state locks.
- Theme spine and quality state: choices alter `trust_meng`, `station_risk`, `ticket_corner_kept`, and `refund_failed_stamp_used`.
- Vertical slice pipeline: CSV, readable preview, QA, engine exports, Character Card V2, and Excel all generated.

## Fixes After First QA
- Added `current_axes`, `active_wants`, `voice_lock`, and `state_history` to all runtime character states.
- Reduced overpacked dialogue textboxes at TW014, TW035, TW043, TW067, and TW074.
- Varied 林桥's line endings so his voice no longer collapses into one-note full stops.
- Removed comma-fragmenting from 孟雨's core plea at TW043.
- Updated the Excel builder row-type dropdown to include `thought`.

## Result
- Final QA: 0 errors, 0 warnings.
- Script rows: 87.
- Dialogue rows: 59.
- Thought rows: 10.
- Choices: 2 with resolved branch labels and visible state effects.
