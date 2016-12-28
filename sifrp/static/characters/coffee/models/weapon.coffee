class Weapon extends models.Item
    directory: Rulebook.weapons

    defaults:
        supporting: false
        left: false
        right: false
        carried: true
    
    validate: =>
        equipped = @get('left') or @get('right')
        if equipped and not @get 'carried'
            throw new Error "You can't hold a weapon you're not carrying"
        if @get('supporting') and not equipped
            throw new Error "You can't attack with a weapon you're not holding"
        if @get('supporting') and not @get('qualities')['off-hand']
            throw new Error "You can only support with off-hand weapons"

    initialize: =>
        @collection.bind 'change:left', (model, equipped) =>
            return unless equipped
            if model is this then @set {carried: true}, silent: true
            else if @get 'left' then @set {left: false}, silent: true

        @collection.bind 'change:right', (model, val) =>
            return unless equipped
            if model is this then @set {carried: true}, silent: true
            else if @get 'right' then @set {right: false}, silent: true

        @bind 'change:carried', (model, carried) =>
            if not carried then @set {
                right: false
                left: false
                supporting: false
            }, silent: true

    bulk: => @get('qualities').bulk or 0


class models.Weapons extends Backbone.Collection
    model: Weapon
