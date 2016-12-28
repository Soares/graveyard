" Bound: a A b e f g h l n o q r s S t w W ? =
" Modes: leader-go leader-fold
" TODO: Manually set CtrlP's ,e. Split ,b* into leader-buffer.

" Key | Command
" a | ack
" A » Extended ack mode
" Aa	Ack add
" Af	Ack file
" AF	Ack add file
" Aw	Ack word
" b » leader-buffer
" bp	buffer previous
" bn	buffer next
" bt	buffer toggle
" bc	buffer close (don't move windows)
" bC	buffer close! (don't move windows)
" be	buffer edit (CtrlP buffer)
" bl	buffer list
" bx	buffer close (allow entry of #)
" bX	buffer close! (allow entry of #)
" B |
" c |
" C |
" d » diff mode
" dd	diff done
" dd	diffget and update
" dm	diffget from merge
" dn	diff next
" dp	diff prev
" dt	diffget from target
" du	diffput and update
" D |
" e | CtrlP buffer
" E |
" f | Fold html tag
" F |
" g » git mode
" ga	Git commit amend
" gb	Git branch
" gc	Git commit
" gd	Git diff
" go	Git checkout
" gs	Git status
" gt	Git5 track
" gw	Gwrite
" G |
" h | Toggle hidden characters
" H |
" i |
" I |
" j |
" J |
" k |
" K |
" l » long line management
" ll	toggle long line highlighting
" ln	jump to next long line
" lp	jump to previous long line
" L |
" m |
" M |
" n | Rotate number style
" N |
" o | CtrlP open
" O |
" p |
" P |
" q | CtrlP quickfix
" Q |
" r | Check syntax
" R |
" s | substitute word under cursor
" S » session management
" So	open session
" Ss	save session
" Sx	delete session
" t | CtrlP tag
" T |
" u |
" U |
" v |
" V |
" w | » trailing whitespace management.
" W | Toggle writer mode.
" x |
" X |
" y |
" Y |
" z |
" Z |
" 0 |
" 1 |
" 2 |
" 3 |
" 4 |
" 5 |
" 6 |
" 7 |
" 8 |
" 9 |
" ! |
" @ |
" # |
" $ |
" % |
" ^ |
" & |
" * |
" ( |
" ) |
" [ |
" ] |
" { |
" } |
" ' |
" " |
" ` |
" ~ |
" - |
" _ |
" / |
" ? | Toggle search highlighting
" \ |
" | |
" = » Tabloid mode.
" ==	Tabloid Fix
" =n	Tabloid Next
" =p	Tabloid Prev
" =t	Change file to tabs
" =s	Change file to spaces
" + |
" ; |
" : |
" . |
" > |
" , |
" < |
" ⏎ |
" → |
" █ |

exe 'noremap <unique> <leader>aa :Ack '
exe 'noremap <unique> <leader>ad :Ackvanced a '
exe 'noremap <unique> <leader>af :Ackvanced f '
exe 'noremap <unique> <leader>ag :Ackvanced af '
noremap <unique> <leader>ak :Ack<CR>
noremap <unique> <leader>as :Ackvanced w <C-R>/
exe 'noremap <unique> <leader>aw :Ackvanced w '
noremap <unique> <leader>bd :Bclose<CR>
noremap <unique> <leader>bD :Bclose!<CR>
noremap <unique> <leader>bn :bn<CR>
noremap <unique> <leader>bp :bp<CR>
noremap <unique> <leader>bl :ls<CR>
noremap <unique> <leader>bt :b#<CR>
noremap <unique> <leader>dd :only<CR>
noremap <unique> <leader>dg :diffget<CR>:diffupdate<CR>
noremap <unique> <leader>dm :diffget //3<CR>:diffupdate<CR>
noremap <unique> <leader>dn ]c
noremap <unique> <leader>dp [c
noremap <unique> <leader>dt :diffget //2<CR>:diffupdate<CR>
noremap <unique> <leader>du :diffput<CR>:diffupdate<CR>
noremap <unique> <leader>e :CtrlPBuffer<CR>
noremap <unique> <leader>ft Vatzf
noremap <unique> <leader>ga :Gcommit --amend<CR>
noremap <unique> <leader>gb :Git branch<CR>
noremap <unique> <leader>gd :Gdiff<CR>
noremap <unique> <leader>gw :Gwrite<CR>
exe 'noremap <unique> <leader>go :Git checkout '
noremap <unique> <leader>gs :Gstatus<CR>
noremap <unique> <leader>gu :Git push origin master
noremap <unique> <leader>h :set list!<CR>
" noremap <unique> <leader>ll :LongLineToggle<CR>
" noremap <unique> <leader>ln :LongLineNext<CR>
" noremap <unique> <leader>lp :LongLinePrev<CR>
noremap <unique> <leader>n :Nu<CR>
noremap <unique> <leader>o :CtrlP<CR>
noremap <unique> <leader>q :cclose<CR>:CtrlPQuickfix<CR>
noremap <unique> <leader>r :w<CR>:SyntasticCheck<CR>
noremap <unique> <leader>s :%s/\<<C-R><C-W>\>/
execute 'noremap <unique> <leader>So :OpenSession '
execute 'noremap <unique> <leader>Ss :SaveSession '
execute 'noremap <unique> <leader>Sx :DeleteSession '
noremap <unique> <leader>t :CtrlPTag<CR>
" noremap <unique> <leader>wn :TrailGuideNext<CR>
" noremap <unique> <leader>wp :TrailGuidePrev<CR>
" noremap <unique> <leader>wt :TrailGuideToggle<CR>
" noremap <unique> <leader>ww :TrailGuideFix<CR>
noremap <unique> <leader>W :Write<CR>
noremap <unique> <leader>== :TabloidFix<CR>
noremap <unique> <leader>=n :TabloidNext<CR>
noremap <unique> <leader>=p :TabloidPrev<CR>
noremap <silent> <unique> <leader>=s :<C-U>call tabloid#set(1, -1)<CR>
noremap <silent> <unique> <leader>=t :<C-U>call tabloid#set(0, -1)<CR>
noremap <unique> <leader>? :set invhls<CR>
