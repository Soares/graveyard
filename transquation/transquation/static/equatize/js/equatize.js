var equatize = (function(self) {
    var replace = function(match, inner) {
        tex = parse(inner);
        console.log(src(tex));
        return tex ? '<img src="' + src(tex) + '" alt="' + tex + '">' : '';
    };

    var src = function(tex) {
        query = encodeURIComponent(tex);
        return 'http://chart.apis.google.com/chart?cht=tx&chl=' + query;
    };

    var parse = function(inner) {
        return inner;
    };

    self.convert = function(text) {
        return text.replace(/~D([^$]*?)~D/g, replace);
    };

    return self;
})(equatize || {});
