@views = {}

class views.View extends Backbone.FormView
    constructor: (options) ->
        @collection = options?.collection
        super


class views.Dialog extends views.View
    constructor: ->
        options =
            autoOpen: false
            draggable: false
            resizable: false
            modal: true
            width: 400
        options = _.extend options, @options
        buttons = @buttons
        if _.isFunction buttons then buttons = buttons()
        for name, attr of buttons
            if _.isString attr then buttons[name] = @[attr]
        if buttons then options.buttons = buttons
        @el = $(@el).dialog options
        super
    results: =>
    open: (@callback) => @el.dialog 'open'
    close: =>
        @el.dialog 'close'
        results = @results()
        results = [results] unless _.isArray results
        if @callback then @callback results...


class views.Charactered extends views.View
    getModel: (model) -> model
    getCharacter: (reference) -> reference
    reassign: (reference) =>
        @character = @getCharacter reference
        super @getModel reference
        do @bind
    activate: ->
    bind: ->
