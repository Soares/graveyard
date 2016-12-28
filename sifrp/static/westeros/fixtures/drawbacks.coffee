@Rulebook.drawbacks = {}

class @Rulebook.drawbacks.Flaw extends @Rulebook.Drawback
    brief: "You suffer from some malady or weakness."
    description: "When you gain this drawback, select a single ability. You
 gain -1D on all tests involving this ability."
    choose: 'ability'
    isDuplicate: => false
    checkSpecial: (pass, fail) =>
        console.log 'PROBLEM HERE. NEED DEFAULT ABILITIES'
        return unless @ability
        others = @character.get('drawbacks').filter (q) =>
            q.name is 'flaw' and q.ability is @ability
        score = @character.score @ability
        if others.length >= score
            fail "You can't have as many flaws as test dice in one ability"
    affect: (roll) -> roll.subtract 1, 'd'
    events: => "roll:#{@ability}"

class @Rulebook.drawbacks.Nemesis extends @Rulebook.Drawback
    brief: "You have a dire enemy.",
    description: "You acquire a destructive enemy, an individual who holds you
 in utter contempt whether you did something to deserve it or not."
