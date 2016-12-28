class Mount extends models.Item
    directory: Rulebook.mounts

    defaults:
        mounted: false

class models.Mounts extends Backbone.Collection
    model: Mount
