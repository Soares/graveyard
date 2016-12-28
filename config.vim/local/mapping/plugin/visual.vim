" Modes: motion select visual-fold visual-go
" Modified: \ : ; < >
" TODO: add v_^O and v_^I

" Differences in visual-block mode are [marked].

" Key |  Command              | Original         | Replacement | Unused/Dup
"   a | around » motion       |                  |             |
"   A | - [After]             |                  |             |
"  ^A |                       |                  |             | ✓
"   b | -                     |                  |             |
"   B | -                     |                  |             |
"  ^B | -                     |                  |             |
"   c | cut                   |                  |             |
"   C | cut lines             |                  |             |
"  ^C | cancel                |                  |             |
"   d | -                     |                  |             |
"   D | delete lines [to end] |                  |             |
"  ^D | -                     |                  |             |
"   e | -                     |                  |             |
"   E | -                     |                  |             |
"  ^E | -                     |                  |             |
"   f | -                     |                  |             |
"   F | -                     |                  |             |
"  ^F | -                     |                  |             |
"   g | » visual-go           |                  |             |
"   G | -                     |                  |             |
"  ^G | » select              |                  |             |
"   h | -                     |                  |             |
"   H | -                     |                  |             |
"  ^H | delete highlighted    |                  |             | x
"   i | in » motion           |                  |             |
"   I | - [before]            |                  |             |
"  ^I |                       |                  |             | ✓
"   j | -                     |                  |             |
"   J | join all              |                  |             |
"  ^J |                       |                  |             | ✓
"   k | -                     |                  |             |
"   K | lookup highlighted    |                  |             |
"  ^K |                       |                  |             | ✓
"   l | -                     |                  |             |
"   L | -                     |                  |             |
"  ^L | -                     |                  |             |
"   m | -                     |                  |             |
"   M | -                     |                  |             |
"  ^M | -                     |                  |             |
"   n | -                     |                  |             |
"   N | -                     |                  |             |
"  ^N |                       |                  |             | ✓
"   o | other end             |                  |             |
"   O | other end             |                  |             |
"  ^O | -                     |                  |             |
"   p | paste over            |                  |             |
"   P | paste over            |                  |             |
"  ^P |                       |                  |             | ✓
"   q | -                     |                  |             |
"   Q |                       |                  |             | ✓
"  ^Q |                       |                  |             | ✓
"   r | replace [smart]       |                  |             |
"   R | cut lines             |                  |             | S
"  ^R |                       |                  |             | ✓
"   s | cut                   |                  |             | c
"   S | cut lines             |                  |             |
"  ^S | -                     |                  |             |
"   t | -                     |                  |             |
"   T | -                     |                  |             |
"  ^T | -                     |                  |             |
"   u | lowercase             |                  |             |
"   U | uppercase             |                  |             |
"  ^U | -                     |                  |             |
"   v | » visual              |                  |             |
"   V | » visual line         |                  |             |
"  ^V | » visual block        |                  |             |
"   w | -                     |                  |             |
"   W | -                     |                  |             |
"  ^W | -                     |                  |             |
"   x | delete                |                  |             |
"   X | delete lines [to end] |                  |             | D
"  ^X |                       |                  |             | ✓
"   y | yank                  |                  |             |
"   Y | yank lines            |                  |             |
"  ^Y | -                     |                  |             |
"   z | » visual-fold         |                  |             |
"   Z |                       |                  |             | ✓
"  ^Z | -                     |                  |             |
"   0 | -                     |                  |             |
"   ! | external filter       |                  |             |
"   @ | -                     |                  |             |
"   # | -                     |                  |             |
"   $ | end of line           |                  |             |
"   % | -                     |                  |             |
"   ^ | -                     |                  |             |
"   & |                       |                  |             | ✓
"   * | -                     |                  |             |
"   ( | -                     |                  |             |
"   ) | -                     |                  |             |
"   [ | -                     |                  |             |
"   { | -                     |                  |             |
"  ^[ | -                     |                  |             |
"   ] | -                     |                  |             |
"   } | -                     |                  |             |
"  ^] | jump to tag           |                  |             |
"   ' | -                     |                  | `           |
"   " | -                     |                  |             |
"   ` | -                     |                  | '           |
"   ~ | toggle case           |                  |             |
"   - | -                     |                  |             |
"   _ | -                     |                  |             |
"   / | -                     |                  |             |
"   ? | -                     |                  |             |
"   \ | toggle comment        | nothing          |             |
"   | | -                     |                  |             |
"  ^\ |                       |                  |             | ✓
"   = | reindent              |                  |             |
"   + | -                     |                  |             |
"   ; | command with range    | nothing          |             |
"   : | correct cmd w. range  | command w. range | ;           |
"   . |                       |                  |             | ✓
"   > | shift out [smart]     | shift out        |             |
"   , |                       |                  |             | ✓
"   < | shift in [smart]      | shift in         |             |
"   ⏎ |                       |                  |             | ✓
"   → |                       |                  |             | ✓
"   █ |                       |                  |             | ✓

" / mapped by commenter.
" : falls through to normal mapping.
" ; falls through to normal mapping.
vnoremap < <gv
vnoremap > >gv
