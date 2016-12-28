class Destiny extends views.Charactered
    el: '#destiny'

    links:
        destiny: 'input[name=total]'
        destinySpent: 'input[name=available]'

    events:
        'click button': 'open'

    cleaners:
        destiny: (v) -> (parseInt v) or 0
        destinySpent: (v) ->
            destiny = @character.get 'destiny'
            available = (parseInt v) or 0
            return destiny - available

    displayers:
        destinySpent: (spent) ->
            destiny = @character.get 'destiny'
            return destiny - spent

    bind: => @character.watch 'destiny', @refresh

    refresh: (destiny) =>
        spent = @character.get 'destinySpent'
        @$('input[name=available]').val destiny - spent

    activate: =>
        @$('button').button
            text: false
            icons: primary: 'ui-icon-circle-plus'

    open: => dialog.open(@record)
    
    record: (bought, comment) =>
        if bought
            xp = @character.get 'experience'
            @character.set experience: xp - 50
            comment = 'bought with experience'
        @character.set destiny: @character.get('destiny') + 1
        @character.get('logs').log('destiny', '+1 destiny', comment)


class DestinyDialog extends views.Dialog
    el: '#destiny-dialog'
    results: =>
        bought = @$('#bought-destiny').is ':checked'
        comment = @$('input[name=how]').val()
        return [bought, comment]
    close: =>
        super
        @$('input[name=how]').val('')
    buttons:
        record: 'close'
    initialize: =>
        @$('.options').buttonset()
        @$('#bought-destiny').change -> $('.how').hide()
        @$('#given-destiny').change -> $('.how').show()


dialog = null
$ -> dialog = new DestinyDialog
characters.attach Destiny
