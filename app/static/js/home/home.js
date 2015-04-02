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


    var md = new MobileDetect(window.navigator.userAgent);
    if (md.mobile() == null) {
        var scroll_factor = 0.333333; // Image moves 1/3 as fast as body
        var $image = $('.hero i');
        var $devfestbanner = $('.devfest-banner');
        var $nav = $('nav');
        var $hero = $('.hero');

        var scrollHandler = function() {
            var scrolled = $(window).scrollTop();
            $image.css('transform','translate3d(0px, ' + (scrolled * scroll_factor) + 'px, 0px)');

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
    }
});
