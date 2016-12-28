" Hume message labels
let g:hume#0#ALL = 0
let g:hume#0#MESSAGE = 1
let g:hume#0#INFO    = 2
let g:hume#0#WARNING = 3
let g:hume#0#ERROR   = 4

" Define all variables in a dict globally.
" They will be namespaced under g:<prefix>_
" @param {string} prefix The plugin prefix
" @param {{string: object}} dict A dict of {variable: value} to set.
function! hume#0#def(prefix, dict)
	for l:name in keys(a:dict)
		let l:value = string(a:dict[l:name])
		let l:name = 'g:'.a:prefix.'_'.l:name
		if !exists(l:name)
			exe 'let '.l:name.' = '.l:value
		endif
	endfor
endfunction


" Get the true shiftwidth, regardless of vim version.
if exists('*shiftwidth')
	function! hume#0#sw()
		return shiftwidth()
	endfunction
else
	function! hume#0#sw()
		return &sw
	endfunction
endif


" Checks whether a setting allows a value.
" Designed for settings that can be either global, whitelisted, or blacklisted.
" @param {number|list|dict} setting The setting to check
" @param {string?} value The value to check. Default &ft.
" @return Depends upon the setting:
"		If a number or string, the setting is returned and the value ignored
"		If a list, returns whether or not the value is in the list
"		If a dict, returns setting[value] (defaults to 1)
function! hume#0#check(setting, ...)
	let l:value = a:0 > 0 ? a:1 : &ft
	if type(a:setting) == type([])
		return index(a:setting, l:value) >= 0
	elseif type(a:setting) == type({})
		return get(a:setting, l:value, 1)
	endif
	return a:setting
endfunction
