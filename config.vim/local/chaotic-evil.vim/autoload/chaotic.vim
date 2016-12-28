function! s:sw()
	return &sw > 0 ? &sw : &ts
endfunction

function! chaotic#spaces2tabstop()
	return s:sw() - ((virtcol('$') - 1) % s:sw())
endfunction

function! chaotic#spacealign(line1, line2, sw)
	call s:sub(a:line1, a:line2, '\v(\S.{-})@<=\t', s:spaces(a:sw))
endfunction

function! chaotic#tabalign(line1, line2, sw)
	call s:sub(a:line1, a:line2, '\v(\S.{-})@<= {'.a:sw.'}', '\t')
endfunction
