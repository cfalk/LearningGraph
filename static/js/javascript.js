$('#kwicks-menu').kwicks({ 
  event : 'click', 
  eventClose: 'click', 
  max : 330, 
  spacing : 5, 
  completed : function(){ 
    addMessage('<span class="hilight">something, something,' + 
      'something... com-plete</span>'); 
  } 
});
