class OpenButton extends views.View
    el: '#open'
    events:
        'click': 'open'
    initialize: => $(@el).button icons: primary: 'ui-icon-folder-open'
    open: => dialog.open()


class Loader extends views.View
    events:
        click: 'load'
    constructor: (@character) ->
        render = $('#tmpl-stored').tmpl
            name: character.get('name') or '[unnamed]'
            url: character.url()
            id: character.id
        @el = $ render
        dialog.push @el
        super
    initialize: => @el.button()
    load: =>
        router.navigate @character.url(), true
        dialog.close()



class OpenDialog extends views.Dialog
    el: '#open-dialog'
    focus: (character) => character.watch 'id', @refresh
    refresh: =>
        openable = characters.filter (c) -> c.id?
        if openable.length then @$('.empty').hide()
        else @$('.empty').show()
        _.each(@loaders, (v) -> v.remove()) if @loaders
        @loaders = _.map openable, (c) => new Loader c
    push: (loader) => @$('.characters').append loader


dialog = button = null
characters.bind 'all', (e) ->
    dialog or= new OpenDialog
    if e in ['focus', 'add', 'remove', 'destroy', 'reset'] then dialog.refresh()
$ -> button = new OpenButton
