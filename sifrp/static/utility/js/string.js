String.prototype.title = function() {
    return this.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};
String.prototype.slugify = function() {
    var string = this.replace(/[^\w\s-]/g, '').trim().toLowerCase();
    return string.replace(/[_\s]+/g, '_');
};
String.prototype.decamel = function() {
    return this.replace(/[A-Z][a-z_-]*/g, function(txt) {
        return txt + ' ';
    }).trim();
};
