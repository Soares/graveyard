class Download extends views.Charactered
    el: '#download'
    activate: => $(@el).button icons: primary: 'ui-icon-arrowreturnthick-1-s'
    bind: =>
        @character.bind 'save', => $(@el).show()
        if @character.id? then $(@el).show() else $(@el).hide()

characters.attach Download
