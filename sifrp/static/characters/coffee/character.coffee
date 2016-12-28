@characters = new models.Characters

$ ->
    characters.fetch()
    window.router = new CharacterSpace
    Backbone.history.start pushState: true
