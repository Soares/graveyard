alias aurify="makepkg -s && sudo pacman -U *.pkg.*"
alias bbuild="bookbuilder -a \"Nate Soares\""
alias darknet="eval \"$BROWSER -P fallback -no-remote >/dev/null 2>/dev/null &\""
alias doc="libreoffice"
alias ebook="calibre"
alias gcd="cd ./$(git rev-parse --show-cdup 2> /dev/null)"
alias gs="git status --short"
alias less="less -R"
alias ls="ls --color --hide='$IGNORED_FILES'"
alias mkdir='mkdir -p'
alias music="ncmpcpp"
alias pacman="sudo pacman-color"
alias pdf="evince"
alias pirate="aria2c"
alias so="source"
alias song="cvlc 2>/dev/null&"
alias startx=nicex
alias tmux=$tmux
alias view="feh -F"
alias vim=$vim

qfind() { find . -iname "*$1*" }

function chpwd() {
    emulate -L zsh
    ls
}
