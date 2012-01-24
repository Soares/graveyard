" Vim syntax file
" Language:     CM
" Maintainer:   Nate Soares <nate@natesoares.com>
" Filenames:    *.cm
   

if exists("b:current_syntax")
  finish
endif

if !exists("main_syntax")
  let main_syntax = 'cm'
endif

   
runtime! syntax/html.vim
unlet! b:current_syntax
syn include @CSS syntax/css.vim
unlet! b:current_syntax
syn include @JS syntax/javascript.vim
unlet! b:current_syntax
syn include @SASS syntax/sass.vim
unlet! b:current_syntax
   
syn case ignore
syn cluster cmTop contains=cmExtension,cmBegin,cmComment
syn cluster cmTopLevel contains=@cmFunctions,cmSection,@cmElement
syn match cmExtension "^+\h\S*"

hi def link cmExtension Identifier

" Expressions
syn match cmNumber contained "\<\d\+"
syn match cmNumber contained "\<\d*\.\d\+"
syn match cmLookup contained "[a-zA-Z][a-zA-Z0-9_-]*\%(\.[a-zA-Z][a-zA-Z0-9_-]*\)*"
syn region cmString contained start=+L\="+ skip=+\\\\\|\\"+ end=+"+ contains=cmComment,cmInVar,cmVarEnd,Spell keepend
syn region cmString contained start=+L\='+ skip=+\\\\\|\\'+ end=+'+ contains=cmComment,cmInVar,cmVarEnd,Spell keepend
syn region cmRaw start=+[uU]\=\*\*\*+ skip=+\\\*+ end=+\*\*\*+ contains=cmComment
syn region cmRaw4 start=+[uU]\=\*\*\*\*+ skip=+\\\*+ end=+\*\*\*\*+ contains=cmComment
syn match cmInVar contained "$[a-zA-Z][a-zA-Z0-9_-]*\%(\.[a-zA-Z][a-zA-Z0-9_-]*\)*"
syn match cmVarEnd contained "$/"
syn cluster cmExpression contains=cmNumber,cmString,cmLookup,@cmTopLevel

syn match cmComma contained ","
syn match cmDoubleComma contained ",\s*,"

hi def link cmComma Delimiter
hi def link cmDoubleComma Error
hi def link cmNumber Number
hi def link cmString String
hi def link cmRaw String
hi def link cmRaw4 String
hi def link cmInVar Identifier
hi def link cmVarEnd Special
hi def link cmLookup Identifier

" Parameters
syn cluster cmParameters contains=@cmExpression,cmComma,cmDoubleComma

" Attributes
syn match cmBoolFlag contained ":[a-zA-Z0-9_-]\+"
syn match cmAttrName contained "[a-zA-Z][a-zA-Z0-9_-]*" nextgroup=cmAssign
syn match cmAssign contained "=" nextgroup=@cmExpression

syn cluster cmAttributes contains=cmAttrName,cmBoolFlag,cmComma,cmDoubleComma

hi def link cmAttrName Type
hi def link cmAssign Operator
hi def link cmBoolFlag Type

" Top level
syn cluster cmBCluster contains=@cmTopLevel
syn region cmBrackets matchgroup=cmBracketDelimiter start="\[" end="\]" contained contains=@cmBCluster
hi def link cmBracketDelimiter Delimiter

" Elements
syn match cmTag "-[a-zA-Z][a-zA-Z0-9_-]*" contains=htmlTagName,htmlSpecialTagName nextgroup=@cmElemParts
syn cluster cmElemParts contains=cmProperty,cmId,cmElemParams,cmElemAttributes,cmElemMode,cmBrackets
syn cluster cmElement contains=cmTag,cmId,cmProperty

syn match cmProperty "[\.:@][a-zA-Z0-9_-]\+" nextgroup=@cmElemParts
syn match cmId "#[a-zA-Z0-9_-]\+" nextgroup=@cmElemParts

syn match cmElemMode "[/\>]" contained nextgroup=cmElemMode,cmBrackets
syn region cmElemParams matchgroup=cmElemParamsDelimiter start="(" end=")" contained contains=@cmParameters nextgroup=cmElemAttributes,cmBrackets
syn region cmElemAttributes matchgroup=cmElemAttributesDelimiter start="{" end="}" contained contains=@cmAttributes nextgroup=cmElemMode,cmBrackets

hi def link cmTag Statement
hi def link cmProperty Type
hi def link cmId Identifier
hi def link cmElemParamsDelimiter Delimiter
hi def link cmElemAttributesDelimiter Delimiter
hi def link cmElemMode Special

" Functions
syn match cmFunction "%[a-zA-Z][a-zA-Z0-9_-]*" nextgroup=cmParameters,cmFnAttributes,cmBrackets
syn region cmUnnamed1 matchgroup=cmUnnamed start="%(" end=")" contains=@cmParameters nextgroup=cmFnAttributes,cmBrackets
syn region cmUnnamed2 matchgroup=cmUnnamed start="%{" end="}" contains=@cmAttributes nextgroup=cmBrackets
syn region cmUnnamed3 matchgroup=cmUnnamed start="%\[" end="\]" contains=@cmBCluster
syn cluster cmFunctions contains=cmFunction,cmUnnamed1,cmUnnamed2,cmUnnamed3

syn region cmParameters matchgroup=cmParametersDelimiter start="(" end=")" contained contains=@cmParameters nextgroup=cmFnAttributes,cmBrackets
syn region cmFnAttributes matchgroup=cmFnAttributesDelimiter start="{" end="}" contained contains=@cmAttributes nextgroup=cmBrackets

hi def link cmFunction Function
hi def link cmUnnamed Function
hi def link cmFnAttributesDelimiter Delimiter
hi def link cmParametersDelimiter Delimiter

" Sections
syn match cmSection "\*[a-zA-Z][a-zA-Z0-9_-]*" nextgroup=cmSectionMode,cmBrackets

syn match cmSectionMode "[\+-]" contained nextgroup=cmSectionMode,cmBlock

hi def link cmSection Special
hi def link cmSectionMode Special

" Extra
syn match cmError "\$" contained
syn region cmComment start="//" end="$" keepend contains=@Spell
syn match cmEscape "%\(\\\\\|\\\[\|\\\]\|\\{\|\\}\|\\(\|\\)\|\\%\|\\\*\|\\\-\|\\\.\|\\:\|\\\#\|\\@\|\\\+\|\\/\|\\>\|\\v\)"
syn region cmJavascriptBlock matchgroup=cmStartBlock start="^\z(\s*\)-script" end="^\%(\z1\s\+\)\@!" contains=cmElemAttributes,@cmTopLevel,@JS
syn region cmCssBlock matchgroup=cmStartBlock start="^\z(\s*\)-style" end="^\%(\z1\s\+\|\s*$\)\@!" contains=cmElemAttributes,@cmTopLevel,@CSS
syn region cmSassBlock matchgroup=cmStartBlock start="^\z(\s*\)-sass" end="^\%(\z1\s\+\|\s*$\)\@!" contains=cmElemAttributes,@SASS

hi def link cmStartBlock Statement
hi def link cmEscape Special
hi def link cmComment Comment
hi def link cmError Error

syn match cmLeadingSpaces /^\t*\zs \+/
syn match cmTrailingSpaces / \+$/
syn match cmJustTabs /^\t\+$/
hi def link cmJustTabs Underlined
hi def link cmLeadingSpaces Underlined
hi def link cmTrailingSpaces Underlined
highlight Underlined cterm=underline

let b:current_syntax = "cm"

set tabstop=2 sw=2 noet
