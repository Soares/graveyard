class Clone extends views.Charactered
    el: '#clone'
    events:
        click: 'clone'
    activate: => $(@el).button icons: primary: 'ui-icon-circle-plus'
    clone: =>
        serialized = JSON.stringify @character
        clone = characters.add().last()
        parsed = clone.parse JSON.parse serialized
        parsed.name = parsed.name + ' (clone)'
        delete parsed.id
        clone.set parsed
        clone.save()
        router.navigate clone.url(), true
    bind: =>
        @character.bind 'save', => $(@el).show()
        if @character.id? then $(@el).show() else $(@el).hide()

characters.attach Clone
