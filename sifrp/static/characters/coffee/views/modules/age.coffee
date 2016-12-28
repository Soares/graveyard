class Age extends views.Charactered
    el: '#age'

    links:
        age: 'input[name=age]'
    cleaners:
        age: (v) -> (parseInt v) or 21

    events:
        'click button': 'showReference'

    activate: =>
        @$('button').button
            text: false
            icons: primary: 'ui-icon-circle-triangle-s'

    showReference: => views.reference.age.open(@setAge)

    setAge: (age) => @character.set age: age

    bind: => @character.watch 'age', @setType

    setType: (age) =>
        age = models.Age.prototype.parse age
        @$('.type').html "(#{age.name})"


characters.attach Age
