class Age extends views.reference.View
    template: '#tmpl-age-reference'
    context: =>
        _.extend super, num: switch @ref.flaws
            when 1 then 'one'
            when 2 then 'two'
            when 3 then 'three'
            else null
    initialize: =>
        input = @$('[name=choice]')
        if @ref.max?
            slider = @$('.slider').slider
                min: @ref.min
                max: @ref.max
                value: parseInt (@ref.min + @ref.max) / 2
                change: (e, ui) -> input.val(ui.value)
                slide: (e, ui) -> input.val(ui.value)
            input.val slider.slider 'value'
            input.change -> slider.slider 'value', input.val()
        else
            input.val @ref.min
    results: => @$('.input input').val()


class Ages extends views.reference.List
    el: '#age-reference'
    view: Age
    listing: Rulebook.ages


$ -> views.reference.age = new Ages
