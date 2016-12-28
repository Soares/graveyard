class Gender extends views.Charactered
    el: '#gender'

    links:
        isMale: 'input[name=gender]'
    cleaners:
        isMale: (v) -> v is 'male'
    displayers:
        isMale: (v) -> if v then 'male' else 'female'

    bind: => @$('.buttonset').buttonset()

characters.attach Gender
