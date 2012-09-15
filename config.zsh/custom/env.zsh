# XDG Environment XDG fixes
export CCACHE_DIR=$XDG_CACHE_HOME/ccache
export GIT_CONFIG_FILE=$XDG_CONFIG_HOME/git/config
export GNUPGHOME=$XDG_CONFIG_HOME/gnupg
export LESSHISTFILE=$XDG_DATA_HOME/less.hist
export PENTADACTYL_RUNTIME=$XDG_CONFIG_HOME/pentadactyl,$PENTADACTYL_RUNTIME
export XAUTHORITY=$XDG_CACHE_HOME/X11/auth
export ZSH=$XDG_CONFIG_HOME/zsh/oh-my
export _FASD_DATA=$XDG_DATA_HOME/fasd
export BROWSER="firefox -pentadactyl '+u=$XDG_CONFIG_HOME/pentadactyl/pentadactyl.rc'"
local viminfofile=$XDG_DATA_HOME/vim/info
local tmux="tmux -f $XDG_CONFIG_HOME/tmux/config"
local vim="vim -u $XDG_CONFIG_HOME/vim/vim.rc"

if which tmux 2>&1 >/dev/null; then
	if [[ $TERM == $GUI_TERM; ]]; then
		test -z ${TMUX} && eval "$tmux attach-session -d" || eval $tmux
	fi
fi
