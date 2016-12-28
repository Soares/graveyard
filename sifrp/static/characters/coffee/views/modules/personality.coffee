class Personality extends views.Charactered
    el: '#personality'

    links:
        virtue: 'input[name=virtue]'
        vice: 'input[name=vice]'
        motivation: 'input[name=motivation]'

characters.attach Personality
