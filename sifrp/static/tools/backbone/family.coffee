class Backbone.ParentModel extends Backbone.Model
    constructor: (attrs, options) -> super (@parse attrs or {}), options
    create: (type, attrs) => new type attrs, parent: this

    initialize: =>
        super
        data = {}
        for name, type of @children
            child = @get name
            if (not child) or (_.isEmpty child) then data[name] = @create type
        @set data, silent: true

    parse: (attrs) =>
        for name, type of @children
            if attrs[name] not instanceof type
                attrs[name] = @create type, attrs[name]
        return super

    validate: (attrs) =>
        for name, type of @children
            if attrs and attrs[name] and attrs[name] not instanceof type
                return "'#{name}' is not an instance of '#{type}'"

    eachChild: (fn) =>
        for name, child of @children
            fn @get name
