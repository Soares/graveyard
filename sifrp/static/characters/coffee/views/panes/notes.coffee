class Notes extends views.Charactered
    el: '#notes'
    activate: => $(@el).tabs()
    links:
        notes: '#general'
        family: '#family'
        allies: '#allies'
        enemies: '#enemies'
        acquaintances: '#acquaintances'
        history: '#history'

characters.attach Notes
