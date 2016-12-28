" Modified: J L Q S T U W \
" Modes: insert-go insert-x
" TODO: Manually set snipmate's commands

" Key | Command                   | Original         | Replacement | Unused/Dup
"  ^A | insert last inserted text |                  |             |
"  ^B |                           |                  |             | tmux
"  ^C | cancel insert             |                  |             |
"  ^D | delete indent             |                  |             |
"  ^E | copy-from-above           |                  |             |
"  ^F | retab line                |                  |             |
"  ^G | » insert-go               |                  |             |
"  ^H | delete                    |                  |             | ←
"  ^I | insert a tab              |                  |             |
"  ^J | remove line               | newline          | ⏎           |
"  ^K | digraph mode              |                  |             |
"  ^L | add indent                | normal mode      | esc         |
"  ^M | newline                   |                  |             | ⏎
"  ^N | omnicomplete next         |                  |             |
"  ^O | run one command           |                  |             |
"  ^P | omnicomplete prev         |                  |             |
"  ^Q | delete to 0               | i^V              | i^V         |
"  ^R | dump register             |                  |             |
"  ^S | Down the tag stack        | » surround mode  | i^Gs        |
"  ^T | Up the tag stack          | add indent level | i^L         |
"  ^V | enter unicode             |                  |             |
"  ^U | delete entered text       | ^U w/o undobreak | ^U          |
"  ^W | back word                 | ^W w/o undobreak | ^W          |
"  ^X | » insert-x                |                  |             |
"  ^Y | insert from below         |                  |             |
"  ^Z | suspend                   |                  |             |
"  ^@ | insert last text » normal |                  |             |
"  ^^ | toggle language map       |                  |             |
"  ^[ | escape                    |                  |             |
"  ^] | Trigger abbreviation      |                  |             |
"  ^\ | Snippet expansion         | exit insert mode | ^[          |
"  ^█ | insert last inserted text |                  |             | i^A

inoremap <C-J> <C-U>
inoremap <c-L> <C-T>
inoremap <C-Q> <ESC>v0d
inoremap <C-S> <C-O><C-]>
inoremap <C-T> <C-O><C-T>
" <C-\> set by g:snips_trigger_key
inoremap <C-U> <C-G>u<C-U>
inoremap <C-W> <C-G>u<C-W>
