$(document).ready(function () {
            $(".carousel-item").hover(function(){ $(".carousel-caption").hide();
              $(".carousel-caption").css('visibility', 'visible');
              $(".carousel-caption").stop().fadeIn(1000) },
              function(){   $(".carousel-caption").stop().fadeOut(800, function() {
                            $(".carousel-caption").css('visibility', 'hidden'); }) });
        });