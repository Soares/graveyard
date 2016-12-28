class Glory extends views.Charactered
    el: '#glory'

    links:
        glory: 'input'

    cleaners:
        glory: (v) -> (parseInt v) or 0

    events:
        'click button': 'open'

    activate: =>
        @$('button').button
            text: false
            icons: primary: 'ui-icon-circle-plus'

    record: (comment) =>
        @character.set glory: @character.get('glory') + 1
        @character.get('logs').log('glory', '+1 glory', comment)

    open: => dialog.open(@record)


class GloryDialog extends views.Dialog
    el: '#glory-dialog'
    results: => @$('input').val()
    buttons:
        record: 'close'


dialog = null
$ -> dialog = new GloryDialog
characters.attach Glory
