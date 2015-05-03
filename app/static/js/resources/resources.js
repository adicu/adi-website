$(function() {

    $('.slideto').click(function(e) {
        e.preventDefault();
        id = $(this).attr('href');
        $('html,body').animate({
          scrollTop: $(id).offset().top
        }, 200  );
    });

    var md = new MobileDetect(window.navigator.userAgent);
    if (md.mobile() == null) {
        var $wrapper = $('.sidebar-wrapper .full');
        var $sidebar = $('.sidebar');
        var $inner = $('.sidebar .inner');
        var $navbar = $('.navbar');

        $(window).scroll( function(e) {
            if ($(window).scrollTop() > $wrapper.offset().top - 80) {
                $navbar.addClass('up');
            } else {
                $navbar.removeClass('up');
            }
            if ($(window).scrollTop() > $wrapper.offset().top ) {
                $sidebar.addClass('fixed');
            } else {
                $sidebar.removeClass('fixed');
            }

            var bottomOfSidebar = $inner.offset().top + $inner.height();
            var bottomOfSidebarWrapper = $wrapper.offset().top + $wrapper.height();
            var topOfSidebar = $inner.offset().top;
            var topOfVisibleWindow = $(window).scrollTop();

            if (!$sidebar.hasClass('bottom') && bottomOfSidebar > bottomOfSidebarWrapper){
                $sidebar.addClass('bottom');
            } else if (topOfSidebar > topOfVisibleWindow) {
                $sidebar.removeClass('bottom');
            }


        });
    }

    $('a[href="#set-track"]').click(function(e) {
        e.preventDefault();

        if ($(this).parent().hasClass('on')) {
            $('.on').removeClass('on');
            $('.in-track').removeClass('in-track');
            return;
        }

        topics = $(this).data('topics').split(',');
        $('.on').removeClass('on');

        $(this).parent().addClass('on');
        for(var i = 0; i < topics.length; i++) {
            $('#'+topics[i]).addClass('on');
            $('.sidebar li[data-topic="' + topics[i] + '"]').addClass('on');
        }
        $('.topic, .topics li, .tracks li, .sidebar').addClass('in-track');
    });
});