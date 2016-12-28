class AbilityRequirement
    constructor: (@abilities) ->

    valid: (character) =>
        for ability, test of @abilities
            if _.isArray test
                [min, specialties] = test
                for specialty, val of specialties
                    if character.score(ability, specialty) < val then continue
            else min = test
            if character.score(ability) >= min then return true
        return false

    _renderReq: (ability, test) ->
        [min, specialties] = if _.isArray test then test else [test, false]
        string = "#{ability.title()} #{min}"
        if specialties
            bonuses = ("#{k.title()} #{v}B" for k, v of specialties).sort()
            return "#{string} (#{bonuses.join(', ')})"
        return string

    toString: => (@_renderReq k, v for k, v of @abilities).sort().join(' or ')


class Quality extends Backbone.Model
    initialize: (attrs, options) =>
        if @choose is 'ability' then @choose = ability: true
        else @choose = {} unless @choose

    assign: (@character) =>

    defaults:
        enabled: true

    similar: =>
        @character.get('benefits').filter (q) => q.get('name') is @get('name')

    attach: =>
        @character.bind(event, @[fn]) for fn, event of @_events()

    detach: =>
        @character.unbind(event, @[fn]) for fn, event of @_events()

    destroy: =>
        do @detach
        super

    check: (pass, fail) =>
        @checkAbilities pass, fail
        @checkBenefits pass, fail
        @checkAttributes pass, fail
        @checkSpecial pass, fail
        if @isDuplicate() then fail 'You already have this quality'
        return this

    isDuplicate: =>
        name = @get 'name'
        qs = @character.get('benefits').filter (q) => q.get('name') is name
        for attr in ['ability', 'specialty', 'weapon', 'unique']
            if @choose[attr] then qs = _.filter qs, (q) => q[attr] = @[attr]
        return qs.length

    renderUnique: (str) -> str.title()

    checkAbilities: (pass, fail) =>
        for req in @_requirements 'abilities'
            req = new AbilityRequirement req
            if req.valid @character then pass(req) else fail(req)

    checkBenefits: (pass, fail) =>
        benefits = @character.get 'benefits'
        normalize = (name) -> name.decamel().toLowerCase()
        for name in @_requirements 'benefits'
            name = normalize(name)
            similar = benefits.find((b) -> normalize(b.get 'name') is name)
            if similar then pass(name.title()) else fail(name.title())

    checkAttributes: (pass, fail) =>
        for [attr, test, msg] in @_requirements 'attributes'
            if test @character.get attr then pass(msg) else fail(msg)

    checkSpecial: ->

    hasRequirements: => !!@requirements

    _events: =>
        events = @events
        if _.isFunction events then events = events()
        if _.isString events then events = affect: events
        return events

    _requirements: (attr) =>
        reqs = @requirements?[attr]
        if _.isArray reqs then reqs
        else if reqs then [reqs]
        else []


class @Rulebook.Benefit extends Quality
    _checkBenefits: =>
        benefits = @character.get 'benefits'
        if isHeritage(this) and benifits.any isHeritage
            @_fail 'You already have a heritage quality'
        super

class @Rulebook.Drawback extends Quality
