// A simple module to replace `Backbone.sync` with *localStorage*-based
// persistence. Storage comes with a .nextid function to assign ids to
// objects. Objects without ids are given ids, and saved as JSON
// on *localStorage*.
(function() {

    // Our Store is a collection of json objects in *localStorage*. Create it
    // with a meaningful name, like the name you'd give a table.
    // The store reserves right to that name as a key in local storage and
    // to any key that starts with `name` and a hyphen (for saving models)
    // or with `name` and a colin (for saving metadata). For example,
    // if you make a Store named `myStore` then names like `myStore:counter`
    // and `myStore-modelid` are off limits and reserved for the Store.
    Backbone.Store = function(name) {
        this.name = name;
        var store = localStorage.getItem(this.name);
        this.id = localStorage.getItem(this.name + ':counter') || 1;
        this.records = (store && store.split(",")) || [];
    };

    _.extend(Backbone.Store.prototype, {

        // Get the next id for the store.
        // Ids are unique within the store, but ids are reused between stores
        nextid: function() {
            var next = '' + (this.id++);
            localStorage.setItem(this.name + ':counter', this.id);
            return next;
        },

        // Save the current state of the **Store** to *localStorage*.
        save: function() {
            localStorage.setItem(this.name, this.records.join(","));
        },

        // Add a model, giving it a unique id if it doesn't have an id already
        // Id's will be unique within the store, but different stores
        // will reuse the same ids.
        create: function(model) {
            if (!model.id) model.set({id: this.nextid()});
            localStorage.setItem(this.name+"-"+model.id, JSON.stringify(model));
            this.records.push(model.id.toString());
            this.save();
            return model;
        },

        // Update a model by replacing its copy in `this.data`.
        update: function(model) {
            localStorage.setItem(this.name+"-"+model.id, JSON.stringify(model));
            if (!_.include(this.records, model.id.toString())) this.records.push(model.id.toString()); this.save();
            return model;
        },

        // Retrieve a model from `this.data` by id.
        find: function(model) {
            return JSON.parse(localStorage.getItem(this.name+"-"+model.id));
        },

        // Return the array of all models currently in storage.
        findAll: function() {
            return _.map(this.records, function(id){return JSON.parse(localStorage.getItem(this.name+"-"+id));}, this);
        },

        // Delete a model from `this.data`, returning it.
        destroy: function(model) {
            localStorage.removeItem(this.name+"-"+model.id);
            this.records = _.reject(this.records, function(record_id){return record_id == model.id.toString();});
            this.save();
            return model;
        }

    });

    // Override `Backbone.sync` to use delegate to the model or collection's
    // *localStorage* property, which should be an instance of `Store`.
    Backbone.sync = function(method, model, options) {
        var resp;
        var store = model.localStorage || model.collection.localStorage;

        if(!store) {
            throw new Error("Storage instance not found for " + model);
        }

        switch (method) {
            case "read":    resp = model.id ? store.find(model) : store.findAll(); break;
            case "create":  resp = store.create(model);                            break;
            case "update":  resp = store.update(model);                            break;
            case "delete":  resp = store.destroy(model);                           break;
        }

        if (resp) {
            options.success && options.success(resp);
        } else {
            options.error && options.error("Record not found");
        }
    };
})();
