class Saver extends views.Charactered
    bind: =>
        @character.bind 'change', @save
        @character.eachChild (c) =>
            if c instanceof Backbone.Model
                c.bind 'change', @save
            else if c instanceof Backbone.Collection
                c.bind 'add', (m) =>
                    m.bind 'change', @save
                    do @save
                c.bind 'remove', @save
                c.each (m) => m.bind 'change', @save
    save: =>
        if @character.id then return @character.save()
        if not @character.get 'name' then return
        @character.save()
        router.navigate @character.url()

characters.attach Saver
