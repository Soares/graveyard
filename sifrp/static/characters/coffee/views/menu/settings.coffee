class SettingsButton extends views.View
    el: '#settings'
    events:
        click: 'open'
    initialize: =>
        $(@el).button
            text: false
            icons: primary: 'ui-icon-wrench'
    open: => dialog.open()


class SettingsDialog extends views.Dialog
    el: '#settings-dialog'
    initialize: => $('.buttonset').buttonset()


dialog = button = null
$ ->
    button = new SettingsButton
    dialog = new SettingsDialog


class SettingsHandler extends views.Charactered
    el: '#settings-dialog'
    links:
        autosave: 'input[name=autosave]'
    cleaners:
        autosave: (val) -> val is 'on'
    displayers:
        autosave: (val) -> if val then 'on' else 'off'
characters.attach SettingsHandler
