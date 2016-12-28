class actions.Attack extends actions.Pool
    constructor: (character, @weapon) ->
        super character, @weapon.ability(), @weapon.get('specialty')
