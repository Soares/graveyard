$.validator.addMethod('zipcode', function(value, element) {
    return this.optional(element) || value.match(/^\d{5}(-\d{4})?$/);
}, 'Please enter a valid zip code');
$.validator.addMethod('checked', function(value, element) {
    return $(element).is(':checked');
}, 'You must check this checkbox');

$.validator.setDefaults({
    errorElement: 'li',
    wrapper: 'ul class="errorlist"',
    errorPlacement: function(error, element) {
        var next = element.parents('td').next();
        next.append(error);
    },
});
