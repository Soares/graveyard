let s:cachedir = empty($XDG_CACHE_HOME) ? $HOME . '/.cache' : $XDG_CACHE_HOME
let s:themefile = s:cachedir . "/terminal_theme"

function! theme#Solarize()
	syntax enable

	let g:solarized_termcolors=256
	let g:solarized_termtrans=1
	let g:solarized_italic=1

	try
		colo solarized
	catch /E185/
		echomsg "Solarized theme is not installed."
	endtry
endfunction

function! theme#Light()
	set background=light
	call theme#Solarize()
endfunction

function! theme#Dark()
	set background=dark
	call theme#Solarize()
endfunction

function! theme#Detect()
	if $TERM == $TRUE_TERM
		colo elflord
		return
	endif

	let l:theme = "Solarized Light"
	if l:theme == "Solarized Dark"
		call theme#Dark()
	else
		call theme#Light()
	endif
endfunction

call theme#Detect()
