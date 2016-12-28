class actions.Pool
    constructor: (@character, @ability, @specialty) ->
        if not character then throw 'wtf'
        @d = @character.score @ability
        @b = if @specialty then @character.score @ability, @specialty else 0
        @r = 0

    add: (amount, to) =>
        if not to then @r += amount
        else if to is 'd' then @d += amount
        else if to is 'b' and amount >= -@b then @b += amount
        else throw new Error "Can't add to #{to} in dice pool"

    subtract: (amount, to) => @add(-amount, to)

    roll: =>
        if @specialty then name = "#{@specialty.title()} (#{@ability.title()})"
        else name = @ability.title()
        window.roll name, @d, @b, @r
