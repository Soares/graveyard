class Log extends views.panes.Model
    singular: 'log'
    areYouSure: 'Are you sure? Removing a log entry does not undo the logged
                  action, and there is no way to un-remove a log entry.'
    links:
        comment: 'input.comment'


class Logs extends views.panes.List
    el: '#logs'
    getModel: (character) -> character.get 'logs'
    push: (log) => $(@el).prepend log
    view: Log


characters.attach Logs
