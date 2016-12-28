class New extends views.Charactered
    el: '#new'
    events:
        click: 'reset'
    activate: =>
        $(@el).button icons: primary: 'ui-icon-document'
    bind: =>
        @character.bind 'save', => $(@el).show()
        if @character.id? then $(@el).show() else $(@el).hide()
    reset: =>
        console.log 'navigating', characters.url
        router.navigate characters.url, true

characters.attach New
