" Modified: 0 $ → █
" Modes: window-go

" TODO: W g ^] ] } f F		^Wg^] is like ^W^] with tabs (etc.)
" TODO: ^WZ → close previous window

" Key |  Command              | Original         | Replacement | Unused/Dup
"   a |                       |                  |             | ✓
"   A |                       |                  |             | ✓
"   b | → bottom right window |                  |             |
"   B |                       |                  |             | ✓
"   c | Close window          |                  |             |
"   C |                       |                  |             | ✓
"   d | Definition window     |                  |             |
"   D |                       |                  |             | ✓
"   e |                       |                  |             | ✓
"   E |                       |                  |             | ✓
"   f | File split            |                  |             |
"   F | File split w. line #  |                  |             |
"   g | » window-go           |                  |             |
"   G |                       |                  |             | ✓
"   h | → left                |                  |             |
"   H | ⇒ far left            |                  |             |
"   i | Initialization window |                  |             |
"   I |                       |                  |             | ✓
"   j | → down                |                  |             |
"   J | ⇒ all the way down    |                  |             |
"   k | → up                  |                  |             |
"   K | ⇒ all the way up      |                  |             |
"   l | → right               |                  |             |
"   L | ⇒ far right           |                  |             |
"   m |                       |                  |             | ✓
"   M |                       |                  |             | ✓
"   n | New window            |                  |             |
"   N |                       |                  |             | ✓
"   o | Only window           |                  |             |
"   O |                       |                  |             | ✓
"   p | Previous window       |                  |             |
"   P | Prev window or error  |                  |             |
"   q | Quit window           |                  |             |
"   Q |                       |                  |             | ✓
"   r | Rotate down           |                  |             |
"   R | Rotate up             |                  |             |
"   s | split window          |                  |             |
"   S | split window          |                  |             | ^Ws
"   t | → top left window     |                  |             |
"   T | Move to new tab       |                  |             |
"   u |                       |                  |             | ✓
"   U |                       |                  |             | ✓
"   v | vertical split        |                  |             |
"   V |                       |                  |             | ✓
"   w | → down or right, wrap |                  |             |
"   W | → up or left, wrap    |                  |             |
"   x | Exchange window       |                  |             |
"   X |                       |                  |             | ✓
"   y |                       |                  |             | ✓
"   Y |                       |                  |             | ✓
"   z | Close preview windows |                  |             |
"   Z |                       |                  |             | ✓
"   0 | First tab             | nothing          |             |
"   ! |                       |                  |             | ✓
"   @ |                       |                  |             | ✓
"   # |                       |                  |             | ✓
"   $ | Last tab              | nothing          |             | ✓
"   % |                       |                  |             | ✓
"   ^ | Split alt file        |                  |             |
"   & |                       |                  |             | ✓
"   * |                       |                  |             | ✓
"   ( |                       |                  |             | ✓
"   ) |                       |                  |             | ✓
"   [ |                       |                  |             | ✓
"   ] | Split tag             |                  |             |
"   { |                       |                  |             | ✓
"   } | Split tag preview     |                  |             |
"   ' |                       | `                | `           | ✓
"   " |                       |                  |             | ✓
"   ` |                       | '                | '           | ✓
"   ~ |                       |                  |             | ✓
"   - | Decrease height       |                  |             |
"   _ | Set height            |                  |             |
"   / |                       |                  |             | ✓
"   ? |                       |                  |             | ✓
"   \ |                       |                  |             | ✓
"   | | Set width             |                  |             |
"   = | Equalize windows      |                  |             |
"   + | Increase height       |                  |             |
"   ; |                       |                  |             | ✓
"   : |                       |                  |             | ✓
"   . |                       |                  |             | ✓
"   > | Decrease width        |                  |             |
"   , |                       |                  |             | ✓
"   < | Increase width        |                  |             |
"   ⏎ |                       |                  |             | ✓
"   → | Prev tab              | ^Wi              |             |
"   █ | Next tab              | nothing          |             |

noremap <C-W>0 :tabfirst<CR>
noremap <C-W>$ :tablast<CR>
noremap <C-W><Space> :tabnext<CR>
noremap <C-W><Tab> :tabprev<CR>
