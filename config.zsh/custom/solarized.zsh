function light { set_theme "Solarized Light" }
function dark { set_theme "Solarized Dark" }

function set_theme {
	if [[ $SYSTEM == "MAC" ]]; then
		osascript -e "tell application \"Terminal\" to set current settings of window 1 to settings set \"$1\""
	fi

	if [[ $SYSTEM == "LINUX" ]]; then
		local TERMINAL_THEME="`cat $XDG_CACHE_DIR/terminal_theme`"
		if [[ $1 == $TERMINAL_THEME ]]; then; return; fi

		if [[ $1 == "Solarized Light" ]]; then
			xrdb -DSOLARIZED_LIGHT -merge $XDG_CONFIG_HOME/X11/resources
			eval `dircolors $XDG_CONFIG_HOME/dircolors/ansi-light`
		else
			xrdb -DSOLARIZED_DARK -merge $XDG_CONFIG_HOME/X11/resources
			eval `dircolors $XDG_CONFIG_HOME/dircolors/ansi-dark`
		fi

		echo $1 > $XDG_CACHE_DIR/terminal_theme
		killall urxvt
	fi
}
