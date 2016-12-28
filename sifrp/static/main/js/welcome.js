(function() {
    var open = function(cls, fast) {
      $('.advanced.open').hide();
      $('.advanced.' + cls).fadeIn();
      $('.advanced.open, .show.open').removeClass('open');
      $('.' + cls).addClass('open');
    };

    var close = function(cls) {
        $('.advanced.' + cls).fadeOut(function() {
          $('.' + cls).removeClass('open');
        });
    };

    var otherify = function(cls) {
      $('a.show.' + cls).click(function() {
        if($(this).is('.open')) close(cls);
        else open(cls);
      });
    };

    $(function() {
        $('#toolbar button').button();
        $('.advanced button').button();
        $('#do-register').click(function() {
          $('form.login').fadeOut('fast', function() {
            $('form.register').fadeIn('fast').addClass('active');
          });
        });
        $('#do-login').click(function() {
          $('form.register').fadeOut('fast', function() {
            $('form.login').fadeIn('fast').addClass('active');
          });
        });
        otherify('provider');
        otherify('local');
        if($('#invalid')) $('#invalid').next('input').focus();
    });
})();
