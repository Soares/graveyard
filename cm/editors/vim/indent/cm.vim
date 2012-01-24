" Vim indent file
" Language:	CM
" Maintainer:	Nate Soares <nate@natesoares.com>
" Last Change:	2009 Dec 2

if exists("b:did_indent")
  finish
endif
let b:did_indent = 1

setlocal autoindent sw=2 tabstop=2 et
setlocal indentexpr=GetCmIndent()
setlocal indentkeys=o,O,*<Return>

" Only define the function once.
if exists("*GetCmIndent")
  finish
endif

function! GetCmIndent()
  let lnum = prevnonblank(v:lnum-1)
  if lnum == 0
    return 0
  endif
  let line = substitute(getline(lnum),'\s\+$','','')
  let cline = substitute(substitute(getline(v:lnum),'\s\+$','',''),'^\s\+','','')
  let lastcol = strlen(line)
  let line = substitute(line,'^\s\+','','')
  let indent = indent(lnum)
  let cindent = indent(v:lnum)
  let increase = indent + &sw
  if indent == indent(lnum)
    let indent = cindent <= indent ? -1 : increase
  endif


  " -tag properties* args? attributes? mode?
  if line =~ '\v^-\w+([\.:#@](\w|-)+)*(\(.{-}\))?(\{.{-}\})?\>?$'
    if line =~ "^-input" || line =~ "^-meta" || line =~ "^-link" || line =~ "^-img" || line =~ "^-br" || line =~ "^-hr"
      return indent
    endif
    return increase
  " properties+ args? attributes? mode?
  elseif line =~ '\v^([\.:#@](\w|-)+)+(\(.{-}\))?(\{.{-}\})?\>?$'
    return increase
  " %name parameters? attributes?
  elseif line =~ '\v^\%\h\w*(\(.{-}\))?(\{.{-}\})?$'
    return increase
  " %(...) attributes?
  elseif line =~ '^%(.\{-\})\%({.\{-\}})?$'
    return increase
  " %{...}
  elseif line =~ '^%{.\{-\}}$'
    return increase
  " *name mode+ "
  elseif line =~ '^\*[a-zA-Z][a-zA-Z0-9_-]\+[\+-]*$'
    return increase
  elseif line =~ '^\s*$'
    return indent - &sw
  else
    return indent
  endif
endfunction
