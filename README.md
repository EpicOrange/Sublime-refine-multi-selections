# refine-multi-selections

Sublime plugin adding a few commands for acting on selected regions.

- SelectSelectionEdges (cmd-k cmd-s): selects edges of selection
- UndoSelectSelectionEdges (cmd-k cmd-shift-s): undos the above
- FlipSelections (cmd-k cmd-f): flips active edges of selections
- OrientSelections (cmd-k cmd-e): makes active edge the right edge
- DeleteEveryOtherSelection (cmd-alt-backspace): delete every other selection
  - WIP: pressing again will retain every 3[, 4, 5, ...] selections
- InvertSelectionInLine (cmd-i): invert selection, bounded by selected lines

![example](https://user-images.githubusercontent.com/6273197/32586484-a0a425da-c4b7-11e7-9970-bdaa2bfb7898.gif)

## Default keys

    { "keys": ["super+k", "super+s"], "command": "select_selection_edges" },
    { "keys": ["super+k", "super+shift+s"], "command": "undo_select_selection_edges" },
    { "keys": ["super+k", "super+f"], "command": "flip_selections" },
    { "keys": ["super+k", "super+e"], "command": "orient_selections" },
    { "keys": ["super+alt+backspace"], "command": "delete_every_other_selection" },
    { "keys": ["super+i"], "command": "invert_selection_in_line" }


## Installing

1. Copy this folder to `Preferences -> Browse Packages...`