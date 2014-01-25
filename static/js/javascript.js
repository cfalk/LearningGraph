/*$('#kwicks-list').kwicks({ 
  event : 'click', 
  eventClose: 'click', 
  max : 330,
  behavior: 'slideshow', 
  spacing : 5, 
});
*/
$().ready(function () {
    $('#kwicks-list').kwicks({
        maxSize: 400,
        spacing: 0,
        behavior: 'menu'
    });
    $('kwicks-list').kwicks('expand', 0);
});
