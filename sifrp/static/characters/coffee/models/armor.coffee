class Armor extends models.Item
    directory: Rulebook.armor

    defaults:
        equipped: false

    _statsOf: (stats) =>
        if not stats then throw new Error "Equipping non-existant configuration"
        relevant = {}
        for stat in ["soak", "penalty", "bulk", "weight"]
            if not stats[stat] then throw new Error "Armor #{stats} has no #{stat}"
            relevant[stat] = stats[stat]
        return relevant

    initialize: =>
        @bind 'change:equipped', =>
            style = @get 'equipped'
            if style is true then @set @_statsOf @refrence
            else if _.isString style
                ref = @directory[style]
                if not ref then throw new Error "Can't find armor #{style}"
                @set @_statsOf ref
            else @set @_statsOf style or @reference

        @collection.bind 'change:equipped', (model, equipment) =>
            return unless equipment and model isnt this
            @set {equipped: false}, silent: true


class models.Armors extends Backbone.Collection
    model: Armor
