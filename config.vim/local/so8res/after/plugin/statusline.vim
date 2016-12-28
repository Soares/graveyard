" Should be in 'after', as it may depend upon other plugins.

" Always show the status line.
set laststatus=2
set statusline=


" Buffer number.
set statusline+=%n·
" File type.
set statusline+=%Y


set statusline+=%#sbOk#
" Current git branch
if exists('g:loaded_fugitive')
	set statusline+=%{fugitive#statusline()}
endif
" Existing view files
if exists('g:loaded_viewport')
	set statusline+=%{viewport#status#info()}
endif
" Current indentation, if sane
if exists('g:loaded_tabloid')
	set statusline+=%{tabloid#status#info()}
endif


set statusline+=%#sbNotify#
" Modified file
set statusline+=%m
" File is read-only
set statusline+=%r
" Existing view files
if exists('g:loaded_viewport')
	set statusline+=%{viewport#status#alert()}
endif
" File mixes tabs and indents on purpose
if exists('g:loaded_tabloid')
	set statusline+=%{tabloid#status#alert()}
endif


set statusline+=%#sbWarning#
" fileformat is not unix
set statusline+=%{&ff!='unix'?'['.&ff.']':''}
" File is not UTF-8
set statusline+=%{(&fenc!='utf-8'&&&fenc!='')?'['.&fenc.']':''}
" Paste is set
set statusline+=%{&paste?'[paste]':''}
" Trailing whitespace
if exists('g:loaded_trailguide')
	set statusline+=%{trailguide#status#warning()}
endif
" Line too long
if exists('g:loaded_longline')
	set statusline+=%{longline#status#warning()}
endif


set statusline+=%#sbError#
" Tabbing is set incorrectly
if exists('g:loaded_tabloid')
	set statusline+=%{tabloid#status#error()}
endif
" Errors detected
if exists('g:loaded_syntastic_plugin')
	set statusline+=%{SyntasticStatuslineFlag()}
endif


" Reset style.
set statusline+=%*
" Move to left side.
set statusline+=%=


" Show the highlight group.
set statusline+=%{synIDattr(synID(line('.'),col('.'),1),'name')}·
" column|line/total
set statusline+=%c%V\|%l\/%L
" Position in file
set statusline+=\ %P


if !exists('g:statusline_tab_exempt_filetypes')
	let g:statusline_tab_exempt_filetypes = ['help', 'text']
endif
function! statusline#TabStatus()
	for exemption in g:statusline_tab_exempt_filetypes
		if &ft == exemption | return '' | endif
	endfor

	let tabs = search('^\t', 'nw') != 0
	let spaces = search('^ ', 'nw') != 0

	if tabs && spaces
		let b:statusline_tab_warning =  '[mixed]'
	elseif (spaces && !&et)
		let b:statusline_tab_warning = '[noet]'
	elseif (tabs && &et)
		let b:statusline_tab_warning = '[et]'
	else
		let b:statusline_tab_warning = ''
	endif
	return b:statusline_tab_warning
endfunction
