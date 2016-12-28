matchNum = '(-?\\d+)\\s*'
pluralNameRe = (name) ->
    name = name.replace 'half ', 'half'
    name = name.replace 'half', 'half ?'
    if name.match /y$/ then name.replace /y$/, '(?:y|ies)'
    else name + 's?'
pluralColorRe = (color) => if color is 'gold' then color else color + 's?'


class Denomination
    constructor: (description) ->
        @color = description.color
        @name = description.name
        @value = description.value
        @common = description.common

        if @name.match /y$/ then @plural = @name.replace /y$/, 'ies'
        else @plural = @name + 's'

        if @name.match /^half/
            next = @name.match(/^half ?(.)/)[1]
            @abv = 'h' + next
        else @abv = @color[0] + @name[0]

        parts = [@abv]
        if @common then parts.push @color[0] + '\\b'
        parts.push "(?:#{@color})? " + pluralNameRe @name
        if @common then parts.push pluralColorRe @color
        options = parts.join('|')
        @regex = new RegExp "#{matchNum}(?:#{options})", 'ig'

    parse: (string) =>
        matches = string?.match @regex
        return 0 unless matches
        return _.reduce matches, ((tot, m) -> tot + parseInt m), 0


class Amount
    constructor: (@value, @denomination) ->

    inTermsOf: (other) =>
        common = @commonValue
        used = Math.floor common / other.value
        leftover = common % other.value
        converted = new Ammount used, other
        return [converted, leftover]

    commonValue: => @value * @denomination.value

    toString: => '' + @value + @denomination.abv

    add: (other) => @value += @denomination.parse other.toString()
    subtract: (other) => @value -= @denomination.parse other.toString()


class models.Money
    constructor: (string) -> @parse string
    parse: (string) =>
        @coins = _.map denominations, (d) -> new Amount d.parse(string), d
    value: => _.reduce @coins, ((tot, c) -> tot + c.commonValue()), 0
    toString: => (_.map @coins, (c) -> c.toString()).join(' ')
    add: (money) => _.map @coins, (c) -> c.add(money)
    subtract: (money) => _.map @coins, (c) -> c.subtract(money)
    toJSON: => @toString()


denominations = _.map(Rulebook.money, (desc) -> new Denomination desc)
