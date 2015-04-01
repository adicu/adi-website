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
        var $image = $('.hero i');
        var $devfestbanner = $('.devfest-banner');
        var $nav = $('nav');
        var $hero = $('.hero');
        var didScroll = false;

        var scrollHandler = function() {
            var scrolled = $(window).scrollTop();
            console.log(scrolled);
            $image.css('transform','translate3d(0px, ' + (scrolled/4) + 'px, 0px)');

            if ($devfestbanner !== undefined) {
                if (scrolled > $hero.height()) {
                    $devfestbanner.addClass('up');
                } else if (scrolled  <= 0) {
                    $devfestbanner.removeClass('up');
                }
            }
        }

        $(window).on('scroll', function() {
           window.requestAnimationFrame(scrollHandler);
        });
    }
});
