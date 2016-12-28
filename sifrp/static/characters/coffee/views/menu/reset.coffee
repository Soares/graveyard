areYouSure = "Are you sure you want to reset this character?
              Resetting will clear all comabt and intrigue damage."
    
class Reset extends views.Charactered
    el: '#reset'
    activate: => $(@el).button icons: secondary: 'ui-icon-heart'
    events:
        click: 'reset'
    reset: =>
        confirm
            title: 'Reset character'
            text: areYouSure
            confirm: 'reset'
            =>

characters.attach Reset
