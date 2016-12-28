class models.Logs extends Backbone.Collection
    log: (type, action, comment) =>
        @add type: type, action: action, comment: comment
