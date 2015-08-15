$(function() {
    $('form.subscribe .submit').click(function() {
        $(this).parent('form').submit();
    });

    $('.navbar a').click(function(e) {
        e.stopPropagation();
    });

    $('.navbar').click(function() {
        $('html,body').animate({
          scrollTop: $('html, body').offset().top
        }, 200  );
    });

    // Email regex
    var pattern = new RegExp(/^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i);
    $('footer form input[type="email"]').keyup(function() {
        if (pattern.test($(this).val())) {
            $('footer form').addClass('valid');
        } else {
            $('footer form').removeClass('valid');
        }
    });



    var md = new MobileDetect(window.navigator.userAgent);
    if (md.mobile() == null) {
        var scroll_factor = 0.333333; // Image moves 1/3 as fast as body
        var $image = $('.hero i');
        var $devfestbanner = $('.devfest-banner');
        var $nav = $('nav');
        var $hero = $('.hero');

        var translateY = function(y) {
            return 'translate3d(0px, -' + y + 'px, 0px)'
        }

        var scrollHandler = function() {
            var scrolled = $(window).scrollTop();
            var scrolled = Math.min(scrolled, $image.height());
            $image.css({
                'transform': translateY(scrolled * scroll_factor),
                '-o-transform': translateY(scrolled * scroll_factor),
                '-moz-transform': translateY(scrolled * scroll_factor),
                '-webkit-transform': translateY(scrolled * scroll_factor)
            });

            if ($devfestbanner !== undefined) {
                if (scrolled > $hero.height()) {
                    $devfestbanner.addClass('up');
                } else if (scrolled <= 0) {
                    $devfestbanner.removeClass('up');
                }
            }
        }

        $(window).on('scroll', function() {
           window.requestAnimationFrame(scrollHandler);
        });
        $(window).on('resize', function() {
            window.requestAnimationFrame(scrollHandler);
        })
        window.requestAnimationFrame(scrollHandler);
    }
});
