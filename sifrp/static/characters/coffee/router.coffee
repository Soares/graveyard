class @CharacterSpace extends Backbone.Router
    routes:
        'character/:id/':  'edit'
        'character/':  'new'

    new: -> characters.trigger 'focus', characters.create()

    edit: (id) -> characters.trigger 'focus', characters.get id
