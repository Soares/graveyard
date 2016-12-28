@Rulebook.benefits = {}

class @Rulebook.benefits.AnimalCohort extends @Rulebook.Benefit
    type: 'fate'
    brief: "Your bond with an animal has instilled in it unwavering loyalty, and
 a willingness to defend you."
    description: "Choose one animal from the following list: dog, eagle, horse,
 raven, shadowcat, or wolf. This animal is extremely loyal to you and fights on
 your behalf.  Whenever you roll Fighting tests in combat and your animal is
 nearby, add +1D to your Fighting test. You need never test Animal Handling to
 control your animal. Your Animal Cohort has stats described in the rulebook.
 \n\tShould your animal cohort die, you lose this benefit and the Destiny Point
 you invested.\n\tYou may select other animals (such as a direwolf, for example)
 with the Narrator's permission."
    requirements:
        abilities:
            'animal handling': [3, 'train': 1]
    choose:
        ability: true
        unique:
            name: 'animal'
            options: ['dog', 'eagle', 'horse', 'raven', 'shadowcat', 'wolf']

class @Rulebook.benefits.AxeFighterI extends @Rulebook.Benefit
    type: 'martial'
    brief: "Your swings with axes produce dreadful results"
    requirements:
        abilities:
            'fighting': [4, 'axes': 2]
    events: => "resolve:fighting:axes"
    affect: (roll, result) ->
        b = roll.character.score 'fighting', 'axes'
        if b > roll.b then result.damage += (b - roll.b)

class @Rulebook.benefits.Charismatic extends @Rulebook.Benefit
    type: 'social'
    brief: "You can put your strong personality to good use."
    description: "When you choose this quality, choose a single Persuasion
 specialty. When you test persuasion to use that specialty, add +2 to your test
 result. You may choose this benefit multiple times. Each time, choose a new
 specialty."
    requirements:
        abilities:
            'persuasion': 3
    choose:
        specialty: 'persuasion'
    events: => "roll:persuasion:#{@get 'specialty'}"
    affect: (roll) -> roll.add 2

class @Rulebook.benefits.Magnetic extends @Rulebook.Benefit
    type: 'social'
    brief: "You have a way about you that cultivates alliances and friendships."
    description: "Whenever you defeat a foe using Charm, that foe's disposition
 increases by a number of steps equal to the number of bonus dice you invested in
 Charm (Minimum 2 steps)."
    requirements:
        benefits: 'charismatic'
    events: => "roll:#{@get 'ability'}"
    affect: (roll) -> roll.add 1, 'd'
