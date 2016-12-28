class models.Item extends Backbone.Model
    directory: Rulebook.items
    changeType: => @set @reference
    bulk: => @get('bulk') or 0


class models.Items extends Backbone.Collection
    model: models.Item
