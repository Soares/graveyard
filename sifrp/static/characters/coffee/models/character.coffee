store = new Backbone.Store "store.characters"


class Character extends Backbone.ParentModel
    defaults:
        # Simle stats
        name: ''
        house: ''
        player: ''
        age: 21
        isMale: true,
        experience: 0
        abilityExperience: 210
        specialtyExperience: 80
        destiny: 4
        destinySpent: 0
        glory: 0
        money: new models.Money
        virtue: ''
        vice: ''
        motivation: ''

        # Settings
        experienceMode: 'creation'
        editingAbilities: true
        autosave: true

        # Transient stats
        damage: 0
        fatigue: 0
        injuries: 0
        wounds: 0
        influence: 0
        frustration: 0

        # Secondary stats
        family: ''
        allies: ''
        enemies: ''
        acquaintences: ''
        history: ''
        notes: ''

    children:
        abilities: models.Abilities
        languages: models.Languages
        benefits: models.Benefits
        drawbacks: models.Drawbacks
        weapons: models.Weapons
        armors: models.Armors
        mounts: models.Mounts
        items: models.Items
        logs: models.Logs

    initialize: =>
        super
        @get('armors').bind 'change:equipped', (armor, worn) =>
            if worn then @set armor: armor
            else if armor is @get 'armor' then @set armor: false

        @get('weapons').bind 'change:left', (weapon, equipped) =>
            if equipped then @set left: weapon
            else if weapon is @get 'left' then @set left: false

        @get('weapons').bind 'change:right', (weapon, equipped) =>
            if equipped then @set right: weapon
            else if weapon is @get 'right' then @set right: false

        @get('mounts').bind 'change:mounted', (mount, mounted) =>
            if mounted then @set mount: mount
            else if mount is @get 'mount' then @set mount: false

    alter: (name, number) =>
        attr = new Attribute(this, number)
        @eachChild (c) => c.trigger "alter:#{name}", attr
        return attr

    mapPosessions: (fn) =>
        a = @get('armors').filter(e.get('equipped')).map(fn)
        w = @get('weapons').filter(e.get('carried')).map(fn)
        i = @get('items').filter(e.get('equipped') or e.get('carried')).map(fn)
        return a.concat w, i

    leftHand: =>
        @get('weapons').detect((w)->w.get('equipped') is 'left') or false
    rightHand: =>
        @get('weapons').detect((w)->w.get('equipped') is 'right') or false
    armor: =>
        @get('armors').detect((a)->a.get 'equipped') or false
    mount: =>
        @get('mounts').detect((m)->m.get 'mounted') or false

    pool: (ability, specialty) =>
        pool = new actions.Pool this, ability, specialty
        @eachChild (c) => c.trigger 'alter:roll', pool
        return pool

    baseMovement: =>
        base = if @score('athletics') <= 1 then 3 else 4
        run = @score 'athletics', 'run'
        bonus = Math.min 3, Math.floor run / 2
        @alter 'move', base + bonus

    bulk: => @alter 'bulk', 0
    move: => @baseMovement() - Math.floor @bulk() / 2
    sprint: => @baseMovement() * 4 - @bulk()

    score: (ability, specialty) =>
        score = @get('abilities').score ability, specialty
        if not score? then score = @get('languages').score ability, specialty
        if not score?
            name = "#{ability} (#{specialty || 'no specialty'})"
            throw new Error "Could not find score for #{name}"
        return score

    clear: =>
        abilities = @get 'abilities'
        languages = @get 'languages'
        for [ability, specialties] in Rulebook.abilities
            abilities.create ability, specialties
        for [ability, specialties] in Rulebook.languages
            score = 0 unless ability is 'common tongue'
            languages.create ability, specialties, score
        return this

    url: => if @id then "#{@collection.url}#{@id}/" else null

    watch: (attr, fn) =>
        @bind "change:#{attr}", (c, a) -> fn a, c.previous attr
        fn @get(attr), false



class models.Characters extends Backbone.Collection
    model: Character
    localStorage: store
    create: => @add().last().clear()
    url: 'character/'
    attach: (view) =>
        instance = new view
        activated = false
        @bind 'focus', (c) ->
            instance.activate() unless activated
            activated = true
            instance.reassign c
        return instance
    link: (link) => @bind 'focus', (c) -> new link c
