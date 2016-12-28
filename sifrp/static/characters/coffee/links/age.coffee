class Age extends links.Link
    constructor: (character) ->
        update = @updateExperience character
        character.watch 'age', update

    updateExperience: (character) -> (age, old) ->
        mode = character.get 'experienceMode'
        return unless mode is 'creation'
        return unless old
        age = models.Age.prototype.parse age
        old = models.Age.prototype.parse old
        dx = age.experience - old.experience
        ds = age.specialty - old.specialty
        dd = age.destiny - old.destiny
        xp = character.get('abilityExperience') + dx
        sp = character.get('specialtyExperience') + ds
        dp = character.get('destiny') + dd
        character.set
            abilityExperience: xp
            specialtyExperience: sp
            destiny: dp

characters.link Age
