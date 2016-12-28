Storage.prototype.setObject = function(key, object) {
    this.setItem(key, JSON.stringify(object));
};
Storage.prototype.getObject = function(key) {
    return this.getItem(key) && JSON.parse(this.getItem(key));
};
