class Experience extends views.Charactered
    el: '#experience'

    links:
        experience: 'input.play'
        abilityExperience: 'input[name=ability]'
        specialtyExperience: 'input[name=specialty]'

    cleaners:
        experience: (v) -> (parseInt v) or 0
        abilityExperience: (v) -> (parseInt v) or 0
        specialtyExperience: (v) -> (parseInt v) or 0

    bind: => @character.watch 'experienceMode', @changeMode

    changeMode: (mode) =>
        if mode is 'creation'
            do @$('.creation').show
            do @$('.play').hide
        else if mode is 'play'
            do @$('.creation').hide
            do @$('.play').show

characters.attach Experience
