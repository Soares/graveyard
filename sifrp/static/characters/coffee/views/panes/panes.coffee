views.panes = {}


class views.panes.Model extends views.View
    constructor: (options) ->
        super
        template = $(@template or "#tmpl-#{@singular}")
        @collection = options.collection
        @el = $(template.tmpl @context())
        do @delegateEvents
        @collection.push @el
        @$('button.remove').button
            text: false
            icons: primary: 'ui-icon-circle-close'
        do @activate

    context: => @model.toJSON()
    activate: =>

    events:
        'click button.remove': 'confirmRemove'

    confirmRemove: =>
        confirm
            title: "Delete #{@singular}?"
            text: @areYouSure
            confirm: 'delete'
            =>
                @model.collection.remove @model
                do @remove


class views.panes.List extends views.Charactered
    push: (log) => $(@el).append log
    add: (model) => new @view model: model, collection: this
    bind: =>
        if @views then _.each @views, (v) -> v.remove()
        @views = @model.map @add
        @model.bind 'add', @add

$ ->
    buttonPane = (button) -> $ button.attr 'target'
    fix = (button) ->
        button.addClass 'ui-state-active'
        button.attr 'disabled', true

    center = $ '#center'
    panes = $ '#center > div'
    buttons = $ '#tabs button'
    buttons.button
        icons: primary: 'ui-icon-circle-triangle-w'
    buttons.map ->
        button = $ this
        pane = buttonPane button
        button.click ->
            buttons.removeClass 'ui-state-active'
            buttons.removeClass 'ui-state-hover'
            buttons.removeAttr 'disabled'
            buttons.button 'option', 'icons', primary: 'ui-icon-circle-triangle-w'

            center.effect 'slide', direction: 'up', mode: 'hide', 'fast', ->
                panes.hide()
                pane.show()
            fix button
            center.effect 'slide', direction: 'up', mode: 'show'

            return false

    panes.hide()
    fix $ buttons[0]
    buttonPane($ buttons[0]).show()
