// $(document).ready(function() {
  // $('#navbarDropdown').mouseenter(function() {
    // $('.dropdown-menu').slideToggle(300, "linear");
  // });
  
  // $('.dropdown-menu').mouseleave(function() {
    // $(this).slideToggle(300, "linear");
  // });
// });


var myNav = document.getElementById('mynav');
window.onscroll = function () {
      "use strict";
       if (document.body.scrollTop >= 20 || document.documentElement.scrollTop >= 20 ) {
          myNav.classList.add("nav-colored");
          $('ul.navbar-nav>li.nav-item>a.nav-link').addClass('custom');
          myNav.classList.remove("nav-transparent");
      }
      else {
          myNav.classList.add("nav-transparent");
          myNav.classList.remove("nav-colored");
          $('ul.navbar-nav>li.nav-item>a.nav-link').removeClass('custom');


      }
};


$(".photocover").hover(
  function(){$(this).removeClass("photog")},
  function(){$(this).addClass("photog");}
);

function myFunction() {
  // Get the text field
  var copyText

  copyText.value = "11732301-20010915-00000000";
   // Copy the text inside the text field
  navigator.clipboard.writeText(copyText.value);

} 