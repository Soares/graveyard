abilityExperienceDelta = (prev, score, lang) ->
    cAbility = (score) -> if score is 1 then 40 else if score is 2 then 10
    cLanguage = (score) -> if score is 0 then 10
    cost = if lang then cLanguage else cAbility
    big = Math.max score, prev
    small = Math.min score, prev
    sum = (list) -> _.reduce list, (a, b) -> a + b
    delta = sum ((cost score) or 30 for score in [small...big])
    if score > prev then -delta else delta


class Experience extends links.Link
    constructor: (character) ->
        changeAbility = @changeAbility character
        changeSpecialty = @changeSpecialty character

        abilities = character.get 'abilities'
        abilities.bind 'change', changeAbility
        abilities.each (a) =>
            a.get('specialties').bind 'change', changeSpecialty

        languages = character.get 'languages'
        languages.bind 'change', changeAbility
        languages.each (a) =>
            a.get('specialties').bind 'change', changeSpecialty

    changeAbility: (character) -> (ability) ->
        mode = character.get 'experienceMode'
        return if mode is 'free'
        score = ability.get 'score'
        prev = ability.previous 'score'
        if mode is 'play'
            xp = character.get 'experience'
            xp -= 30 * (score - prev)
            character.set experience: xp
        else
            xp = character.get 'abilityExperience'
            xp += abilityExperienceDelta prev, score, ability.nonstandard?()
            character.set abilityExperience: xp

    changeSpecialty: (character) -> (specialty) ->
        mode = character.get 'experienceMode'
        return if mode is 'free'
        score = specialty.get 'score'
        prev = specialty.previous 'score'
        if mode is 'play' then xp = character.get 'experience'
        else xp = character.get 'specialtyExperience'
        xp -= 10 * (score - prev)
        if mode is 'play' then character.set experience: xp
        else character.set specialtyExperience: xp


characters.link Experience
