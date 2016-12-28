# Wishlist
Automatically reload vimrc on writepost
Make a command to open the vimrc file in a new tab
Viewport: don't save folds after diffing!
An ack command to search for files that contain the string
An ack command to *open* all the files that contain the string
TRAILGUIDE: trailing newlines
VIEWPORT: not on readonly files
Autosplitter based on my heuristics for available space.
Find a way to use ctrlp "raw" mode or make it faster on google.
Figure out window management.
	CtrlP: stop jumping me to the window where it's open.
Add a NewSession command
auto-format on exit. (Q?)
Make `contab -e` / `sudoedit` work nicely.
Figure out window/buffer management.
Consider conque (http://code.google.com/p/conque/)
Consider autochdir
Merge mapping/ into so8res & flesh it out.
Get better auto completion (from tags & language)
Jump to docs command
ssh integration
nmap gV `[v`]
Why isn't your diff tool highlighted?
autocmd BufReadPost fugitive://\* set bufhidden=delete
autocmd User fugitive  \ if fugitive#buffer().type() =~# '^\%(tree\|blob\)$' |  \   nnoremap <buffer> .. :edit %:h<CR> |  \ endif
http://www.reddit.com/r/vim/comments/138rlq/displaying_description_of_code_in_a_split/

# Runtime files that need to be overridden
Vim: allow \\}) to be valid syntax
Java: chokes when ') {' is on different line of function def.

# Forks that need to be made
Syntastic: needs to be re-entrable.
Surround: cs{[ adds spaces {directory}→[ directory ]
CtrlP:
	stop jumping me to the window where it's open.
	ignore doc/tags

# Soares Plugins
Trailguide:
	canonicalize augroups
	add enable/disable
	auto-disable for read-only files
Longline:
	canonicalize automap, augroups
	add enable/disable
Tabloid:
	split off hemorrhoid
	use sw=0 and sts=-1 and stop dickying with them
	canonicalize
Hume:
	Delete from github?
Write a Refactor plugin, replace ,s
Write the 'Terminal' plugin, use env vars (?) instead of terminal\_theme
Write the 'Chaotic Evil' plugin, use tabs for indent & spaces for align

## Upkeep
Remove docs in plugin/ in favor of INFO files
Make sure everyone is ignoring tag files.
Remove #autoloaded vars, they're redundant.
Update vimscripts online.

# Plugins that Caught my eye
LustyBufExplorer (!) (replace ,b)
Tabularize (!)
Tagbar (!)
SuperTab (?)
## Plugins to discover
Some sort of refactor-variable plugin.
Some sort of localrc plugin that looks in .git etc.
https://github.com/artemave/slowdown.vim
Jedi-vim
Ultisnips
## Lower priority
A cool non-solarized theme    (chriskempson/tomorrow-theme, smyck)
Tree undo                     (sjl.bitbucket.org/gundo.vim)
Template manager              (vim-scripts/template.vim)
Swap text                     (Script 3250)
Tab complete searches         (Script 474)
Git old version viewer        (gregsexton.org/2011/05/gitv-range/)
a.vim                         (edit alternate files)
tpope/vim-unimpaired          (f/t to camelCase letter)
tpope/vim-endwise
tpope/vim-abolish
michaeljsmith/vim-indent-object
easymove
ropevim

# Blind Spots
Alternate files
function/block movement commands
Mark and yank rings
Special marks (Bookmarks?)
Signs (Show marks?)
TODO manager (is Ack good enough?)

# Underused Commands
^N ^P
^E ^Y
(motion) a [pwc etc.]
(motion) i [pwc etc.]
K

# Overused Commands
j
k
v

# External TODOs
switch to ack2
export TMP in zshrc
