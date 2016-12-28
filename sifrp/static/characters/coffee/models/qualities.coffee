class Qualities extends Backbone.Collection
    constructor: (attrs, options) ->
        @character = options.parent
        super (@parse attrs or {}), options

    parse: (list) =>
        for object in list
            type = @reference[object.name]
            new type object, character: @character

    _add: (quality) =>
        quality.assign @character
        quality.attach()
        super


class models.Benefits extends Qualities
    reference: Rulebook.benefits


class models.Drawbacks extends Qualities
    reference: Rulebook.drawbacks
