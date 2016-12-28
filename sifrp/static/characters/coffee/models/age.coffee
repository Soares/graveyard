class models.Age
    constructor: (@value, age) -> _.extend this, age
    toString: => @value
    toJSON: => @value
    parse: (value) ->
        return null unless value
        return value if value instanceof Age
        value = (parseInt value) or 0
        for age in Rulebook.ages
            return new Age(value, age) unless age.max
            if age.min < value <= age.max then return new Age(value, age)
