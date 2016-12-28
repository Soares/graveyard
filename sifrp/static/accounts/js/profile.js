(function() {
    var require = function(form, rules, success, error) {
        if(typeof success === "string") success = success(form, success);
        if(typeof error === "string") error = error(form, error);
        return $(form).ajaxForm({
            success: success,
            error: error,
            beforeSubmit: check
        }).validate({rules: rules});
    };

    var success = function(form, message) { return function() {
        $('#oops').hide();
        $('#ok .text').html(message || 'It worked!');
        $('#ok').show().stop().animate({opacity: 100}).fadeOut(15000);
        $('button', form).button('option', 'icons', {primary: 'ui-icon-circle-check'});
    }};

    var error = function(form, message) { return function() {
        $('#ok').hide();
        $('#oops .text').html(message || 'An error occured.');
        $('#oops').show().stop().animate({opacity: 100}).fadeOut(15000);
        $('button', form).button('option', 'icons', {primary: 'ui-icon-alert'});
    }};

    var check = function(data, form) {
        $('button', form).button('option', 'icons', {});
        return $(form).valid();
    };

    $(function() {
        $('#main form .smallbutton').button();
        $('#main form .delbutton').button({icons: {primary: 'ui-icon-circle-close'}});

        require('#name', {}, 'Display name changed.');
        require('#email', {email: 'required email'}, function() {
            success('An activation link has been sent to your email.');
            $('#email input').val('');
        });
        require('#password', {
            password: 'required',
            passconf: {equalTo: '#pass1'}
        }, 'Password set.');
        $('form.email').ajaxForm({
            beforeSubmit: function(data, form) {
                return confirm("Are you sure?\nIf you proceed, you will no longer be able\nto log in using " + $('.name', form).html() + ".");
            },
            success: function(msg, str, data, form) { $(form).parents('.auth').remove(); },
            error: function(msg, str, data, form) { error(form, msg); }
        });
        $('form.external').ajaxForm({
            beforeSubmit: function(data, form) {
                return confirm("Are you sure?\nIf you proceed, you will no longer be able\nto log in using " + $('.name', form).html() + ".");
            },
            success: function(msg, str, data, form) {
                var auth = $(form).parents('.auth');
                $(form).remove();
                if(!$('.external', auth).length) $('.email', auth).removeClass('unkillable');
                if(!$('#rest .external').length) $('#rest').remove();
            },
            error: function(msg, str, data, form) { error(form, msg); }
        });

        require('#update-primary', {}, 'Primary email updated.');
        $('#emails').sortable({
            update: function(e, ui) {
                var first = $('#emails form.email:eq(0)');
                if(first.is('.primary')) return;
                $('#emails form.email.primary').removeClass('primary');
                first.addClass('primary');
                $('#update-primary [name=pk]').val(first.find('[name=pk]').val());
                $('#update-primary').submit();
            }
        });
    });
})();
