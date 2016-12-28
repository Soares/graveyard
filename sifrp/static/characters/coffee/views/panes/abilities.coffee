class Specialty extends views.Charactered
    links:
        score: 'input'

    cleaners:
        score: (val) ->
            val = Math.max 0, ((parseInt val) or 0)
            mode = @character.get 'experienceMode'
            # Specialty dice may not exceed ability dice
            if mode isnt 'free'
                val = Math.min @collection.model.get('score'), val
            return val

    events:
        click: 'roll'

    constructor: (options) ->
        @specialty = options.specialty
        @collection = options.collection
        @el = @render @specialty
        super
        @collection.append @el

    render: (specialty) => $('#tmpl-specialty').tmpl specialty: specialty

    getModel: (specialties) => specialties.get @specialty
    getCharacter: => @collection.character
    bind: =>
        @character.watch 'editingAbilities', @refresh
        @character.watch 'experienceMode', @setBounds

    refresh: (editing) =>
        if editing then $(@el).removeAttr 'disabled'
        else if not @model.get 'score' then $(@el).attr 'disabled', true

    setBounds: (mode) =>
        if mode is 'play' then @$('input').attr('min', @model.get 'score')
        else @$('input').attr 'min', 0
        event = "change:bounds:#{@collection.model.id}:#{@model.id}"
        setter = (val) ->
            if val? then input.attr('max', val) else input.removeAttr 'max'
        @character.trigger event, @model, setter

    roll: =>
        if $('#abilities').is '.editing' then return
        @character.pool(@collection.model.id, @model.id).roll()


class Ability extends views.Charactered
    links:
        score: 'button.ability input'

    cleaners:
        score: (val) ->
            val = Math.max @min(), ((parseInt val) or 0)
            mode = @character.get 'experienceMode'
            if mode is 'play' then val = Math.max @model.get('score'), val
            return val

    events:
        'click button.ability': 'roll'
        'click .opener.opened': 'close'
        'click .opener.closed': 'open'

    constructor: (options) ->
        [@ability, @specialties] = options.ability
        @el = @render @ability
        super
        @collection.append @el
        @views = _.map @specialties, (s) => new Specialty
            specialty: s
            collection: this

    render: (ability) => $('#tmpl-ability').tmpl ability: ability

    append: (specialty) => @$('.specialties').append specialty

    getModel: (abilities) => abilities.get @ability
    getCharacter: => @collection.character
    bind: =>
        specialties = @model.get 'specialties'
        _.each @views, (v) -> v.reassign specialties
        @character.watch 'editingAbilities', @refresh
        @character.watch 'experienceMode', @setBounds

    refresh: (editing) =>
        button = @$('button.ability').removeAttr 'disabled'
        opener = @$('button.opener').removeAttr 'disabled'
        do @close
        unless editing
            button.attr('disabled', true) unless @model.get 'score'
            active = @$('button.specialty:not(:disabled)').length
            opener.attr('disabled', true) unless active

    min: => if @model.nonstandard?() then 0 else 1

    open: => @$('.closed').addClass('opened').removeClass('closed')

    close: => @$('.opened').addClass('closed').removeClass('opened')

    setBounds: (mode) =>
        input = @$ 'button.ability input'
        if mode is 'play' then input.attr('min', @model.get 'score')
        else input.attr 'min', @min()
        if mode isnt 'free' then input.attr('max', 7)
        else input.removeAttr 'max'
        setter = (val) ->
            if val? then input.attr 'max', val else input.removeAttr 'max'
        @character.trigger "change:bounds:#{@model.id}", @model, setter
        return this
    
    roll: =>
        return if $('#abilities').is '.editing'
        @character.pool(@model.id).roll()


class AbilityList extends views.Charactered
    activate: =>
        @views = _.map @abilities, (a) => new Ability
            ability: a
            collection: this

    append: (ability) => $(@el).append ability

    bind: =>
        abilities = @getCollection @character
        _.each @views, (v) -> v.reassign abilities
        @character.trigger 'change:bounds'



class LeftAbilities extends AbilityList
    el: '#standard .left'
    abilities: Rulebook.abilities[0..8]
    getCollection: (c) -> c.get 'abilities'


class RightAbilities extends AbilityList
    el: '#standard .right'
    abilities: Rulebook.abilities[9..]
    getCollection: (c) -> c.get 'abilities'


class LeftLanguages extends AbilityList
    el: '#languages .left'
    languages: true
    abilities: Rulebook.languages[0..7]
    getCollection: (c) -> c.get 'languages'


class RightLanguages extends AbilityList
    el: '#languages .right'
    languages: true
    abilities: Rulebook.languages[8..]
    getCollection: (c) -> c.get 'languages'


class Abilities extends views.Charactered
    el: '#abilities'

    fragments: [
        LeftAbilities
        RightAbilities
        LeftLanguages
        RightLanguages
    ]

    links:
        experienceMode: 'input[name=pool]'
        editingAbilities: 'input[name=editing]'

    cleaners:
        experienceMode: (v) =>
            if v in ['creation', 'play', 'free'] then v else 'creation'
        editingAbilities: (v) => v is 'true'

    displayers:
        editingAbilities: (v) =>
            if v then 'true' else 'false'

    events:
        'click #free-roll': 'freeRoll'

    initialize: =>
        super
        @views = _.map @fragments, (v) => new v

    activate: =>
        _.each @views, (v) -> v.activate()
        $('#edit-abilities, #start-rolling, #free-roll').button()
        $('#experience-pool, #ability-mode').buttonset()

    bind: =>
        _.each @views, (v) => v.reassign @character
        @character.watch 'editingAbilities', @setMode
        @character.watch 'experienceMode', -> $('#experience-pool').buttonset()

    setMode: (editing) =>
        if editing then $(@el).addClass 'editing'
        else $(@el).removeClass 'editing'
        $('#ability-mode').buttonset()

    freeRoll: -> window.roll()


characters.attach Abilities
