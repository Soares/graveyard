roll = (n) -> (Math.ceil Math.random() * 6) for i in [1..n]
sum = (list) -> _.reduce list, ((x, y) -> x + y), 0

class Roller extends Backbone.View
    events:
        'click .diff.up': 'increment'
        'click .diff.down': 'decrement'

    initialize: (options) =>
        @d = @$ '.inputs [name=d]'
        @b = @$ '.inputs [name=b]'
        @r = @$ '.inputs [name=r]'
        if options.d? then @d.val options.d
        if options.b? then @b.val options.b
        if options.r? then @r.val options.r
        @taken = @$ '.results .taken'
        @dropped = @$ '.results .dropped'
        @added = @$ '.results .added'
        @total = @$ '.results .total'
        @el.dialog
            resizable: false
            position: 'center center'
            minWidth: 350,
            buttons:
                Roll: @roll
            close: @remove
        do @roll

    increment: (e, ui) =>
        input = $(e.target).siblings('input')
        input.val parseInt(input.val()) + 1

    decrement: (e, ui) =>
        input = $(e.target).siblings('input')
        val = parseInt(input.val()) - 1
        if input.is('[name!=r]') then val = Math.max(0, val)
        input.val val

    roll: =>
        d = parseInt @d.val()
        b = parseInt @b.val()
        r = parseInt @r.val()
        sign = if r > 0 then '+' else ''
        dice = roll(d + b).sort().reverse()
        taken = dice.slice 0, d
        dropped = dice.slice d
        total = r + sum taken
        @taken.html taken.join(' ')
        @dropped.html dropped.join(' ')
        @added.html "#{sign}#{r or ''}"
        @total.html total


@roll = (title, d, b, r) ->
    template = $ '#roller-template'
    dialog = template.clone()
    dialog.removeAttr 'id'
    console.log 'args are', arguments
    if title? then dialog.attr 'title', title
    template.after dialog
    return new Roller el: dialog, d: d, b: b, r: r
