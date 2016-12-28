class Remove extends views.Charactered
    el: '#remove'
    events:
        click: 'remove'
    activate: ->
        $(@el).button icons: secondary: 'ui-icon-circle-close'
    bind: =>
        if @character.id? then @$('.ui-button-text').html 'Remove'
        else @$('.ui-button-text').html 'Clear'
    remove: =>
        action = if @character.id? then 'remove' else 'clear'
        text = "Are you sure you want to #{action} this character?"
        title = "#{action} character".title()
        $(@el).removeClass 'ui-state-hover'
        confirm title: title, text: text, confirm: action, =>
            @character.destroy()
            router.navigate characters.url, true

characters.attach Remove
