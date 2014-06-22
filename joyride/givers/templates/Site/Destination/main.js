  $(document).ready(function(){
      $(".main").height($(window).height());
      $(".main").width($(window).width());
          $(window).resize(function(){
              $(".main").height($(window).height());
              $(".main").width($(window).width());
      });
  });
  
function scrollNav() {
  $('.nav a').click(function(){  
    //Toggle Class
    $(".active").removeClass("active");      
    $(this).closest('li').addClass("active");
    var theClass = $(this).attr("class");
    $('.'+theClass).parent('li').addClass('active');
    //Animate
    $('html, body').stop().animate({
        scrollTop: $( $(this).attr('href') ).offset().top
    }, 500);
    return false;
  });
  $('.scrollTop a').scrollTop();	
}
scrollNav();


function scrollHome() {
  $('#home').click(function(){  
$(".active").removeClass("active");      
    $(this).closest('li').addClass("active");
    var theClass = $(this).attr("class");
    $('.'+theClass).parent('li').addClass('active');
    //Animate
    $('html, body').stop().animate({
        scrollTop: $( $(this).attr('href') ).offset().top
    }, 500);
    return false;
  });	
}

scrollHome();


function windowH() {
   var wH = $(window).height();

   $('.panel-body').css({height: wH});
}

windowH();