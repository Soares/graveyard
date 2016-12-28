class Specialty extends Backbone.Model
    defaults:
        score: 0


class Specialties extends Backbone.Collection
    model: Specialty

    score: (specialty) => @get(specialty).get 'score'
    create: (specialty, score=0) =>
        spec = new Specialty id: specialty, score: score
        @add spec


class Ability extends Backbone.ParentModel
    defaults:
        score: 2

    children:
        specialties: Specialties


class models.Abilities extends Backbone.Collection
    model: Ability

    score: (ability, specialty) =>
        abil = @get ability
        return null unless abil
        return abil.get 'score' unless specialty
        return abil.get('specialties').score specialty

    create: (ability, specialties, score=2) =>
        abil = new @model id: ability, score: score
        specs = abil.get 'specialties'
        for specialty in specialties
            specs.create specialty
        @add abil


class Language extends Ability
    nonstandard: => @id isnt 'common tongue'
    language: true


class models.Languages extends models.Abilities
    model: Language
