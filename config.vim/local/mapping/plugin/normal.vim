" Modified: Q ^K ^N ^P ^S ' " - _ \ ; : ,
" Modes: autocomplete bracket command comment fold go insert replace restricted
"        visual visual-block window
" TODO: Set comment mode manually.

" Key |  Command              | Original         | Replacement | Unused/Dup
"   a | after charater        |                  |             |
"   A | after line            |                  |             |
"  ^A | add to number         |                  |             |
"   b | back word             |                  |             |
"   B | back WORD             |                  |             |
"  ^B | backwards-scroll      |                  |             |
"   c | change                |                  |             |
"   C | change line           |                  |             |
"  ^C | cancel                |                  |             |
"   d | delete                |                  |             |
"   D | delete line           |                  |             |
"  ^D | Scroll ½ page down    |                  |             |
"   e | end of word           |                  |             |
"   E | end of WORD           |                  |             |
"  ^E | extra lines           |                  |             |
"   f | forward               |                  |             |
"   F | reverse Forward       |                  |             |
"  ^F | scroll page forward   |                  |             |
"   g | » go mode             |                  |             |
"   G | goto                  |                  |             |
"  ^G | Get info              |                  |             |
"   h | left                  |                  |             |
"   H | cursor to Head        |                  |             |
"  ^H | left                  |                  |             | h
"   i | » insert              |                  |             |
"   I | instert before line   |                  |             |
"  ^I | inward jump           |                  |             |
"   j | down                  |                  |             |
"   J | Join lines            |                  |             |
"  ^J | down                  |                  |             | j
"   k | up                    |                  |             |
"   K | lookup                |                  |             |
"  ^K | digraph mode          | nothing          |             |
"   l | right                 |                  |             |
"   L | cursor to Lower       |                  |             |
"  ^L | clear & redraw        |                  |             |
"   m | mark                  |                  |             |
"   M | cursor to Middle      |                  |             |
"  ^M | j and ^               |                  |             |
"   n | next match forward    |                  |             |
"   N | next match backward   |                  |             |
"  ^N | next autocomplete     | j                | j           |
"   o | open line             |                  |             |
"   O | Open line above       |                  |             |
"  ^O | outward jump          |                  |             |
"   p | paste                 |                  |             |
"   P | paste before          |                  |             |
"  ^P | prev autocomplete     |                  |             |
"   q | record                |                  |             |
"   Q |                       | ex mode          |             | ✓
"  ^Q | ^V                    |                  |             | ^V
"   r | replace character     |                  |             |
"   R | » replace mode        |                  |             |
"  ^R | redo                  |                  |             |
"   s | slice                 |                  |             |
"   S | slice line            |                  |             |
"  ^S | down tag stack        | terminal lock    |             |
"   t | 'till forward         |                  |             |
"   T | 'Till reverse         |                  |             |
"  ^T | up tag stack          |                  |             |
"   u | undo                  |                  |             |
"   U | undo line             |                  |             |
"  ^U | scroll ½ page up      |                  |             |
"   v | » visual              |                  |             |
"   V | » visual line         |                  |             |
"  ^V | » visual block        |                  |             |
"   w | word forward          |                  |             |
"   W | WORD forward          |                  |             |
"  ^W | » window              |                  |             |
"   x | delete                |                  |             |
"   X | delete before         |                  |             |
"  ^X | decrement number      |                  |             |
"   y | yank                  |                  |             |
"   Y | yank line             |                  |             |
"  ^Y | scroll buffer down    |                  |             |
"   z | » fold                |                  |             |
"   Z | » restricted          |                  |             | ½
"  ^Z | suspend               |                  |             |
"   0 | first column          |                  |             |
"   ! | filter motion         |                  |             |
"   @ | execute register      |                  |             |
"   # | search backwards      |                  |             |
"   $ | to eol                |                  |             |
"   % | jump to match         |                  |             |
"   ^ | to first used column  |                  |             |
"   & | repeat substitution   |                  |             |
"   * | search forward        |                  |             |
"   ( | forward sentence      |                  |             |
"   ) | backward sentence     |                  |             |
"   [ | » bracket             |                  |             |
"   { | forward paragraph     |                  |             |
"  ^[ | escape                |                  |             |
"   ] | » reverse bracket     |                  |             |
"   } | backward paragraph    |                  |             |
"  ^] | jump to definition    |                  |             | ^S
"   ' | jump to mark          | `                | `           |
"   " | register              |                  |             |
"   ` | jump to mark line     | '                | '           |
"   ~ | toggle case           |                  |             |
"   - | next match            | k and ^          | +           |
"   _ | next match reverse    | modified k and ^ | none        |
"   / | search                |                  |             |
"   ? | search reverse        |                  |             |
"   \ | » comment             | leader           |             |
"   | | to column             |                  |             |
"  ^\ |                       |                  |             | ✓
"   = | realign               |                  |             |
"   + | k non-blank           |                  |             |
"   ; | » command             | prev f/t         |             |
"   : | fix command           | » command        |             |
"   . | repeat                |                  |             |
"   > | shift out             |                  |             |
"   , | leader                | next f/t         |             |
"   < | shift in              |                  |             |
"   ⏎ | j and 0               |                  |             |
"   → |                       |                  |             | ✓
"   █ | l                     |                  |             | l

noremap Q <ESC>
noremap <C-K> a<C-K>
noremap <C-N> i<C-N>
noremap <C-P> i<C-P>
noremap <C-S> <C-]>
noremap ' `
noremap ` '
noremap _ ,
noremap - ;
noremap ; :
noremap : :<C-f>
" mapleader is set in vimrc
