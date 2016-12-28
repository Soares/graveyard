$ ->
    dialog = $('#dialog-confirm').dialog
        autoOpen: false
        modal: true
        width: 400
        resizable: false
        draggable: false

    window.confirm = (options, proceed, cancel) ->
        ok = ->
            dialog.dialog 'close'
            proceed?()
        buttons = {}
        buttons[options.confirm or 'proceed'] = ok
        dialog.html options.text or 'Are you sure?'
        dialog.dialog 'option', 'title', options.title or 'Please confirm'
        dialog.dialog 'option', 'buttons', buttons
        dialog.dialog 'open'
