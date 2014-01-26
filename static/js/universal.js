var badColor = "#FF8080";
var goodColor = "#B3FFFF";

$(document).ready(function() {

 //Function to propogate ribbon messages.
 window.showRibbon = function(message, color, container){
  $(container).append("<div class=\"ribbonMessage\"/ style=\"background-color:"
   + color + ";\">" + message + "</div>");
  setTimeout(function() {
   $(container).children(".ribbonMessage").fadeOut(500, function() {
    $(".ribbonMessage").remove() 
   })
  }, 750+18*message.length); // Make longer messages stay longer.
 }


 // Enable jQuery Auto-Complete
 var node_names;
 function setAutoComplete(object){
  if (node_names !== undefined) {
    $(object).autocomplete({
     source: node_names
    });
  } else {
   $.getJSON("/get_node_names/", function(data) {
    node_names = data;
    $(object).autocomplete({
     source: data
    });
   })
  }
 }
 //Right off the bat, load the autocomplete for 
 setAutoComplete(".autocomplete")

 //Enable jQuery ToolTips (And disable when input is selected)
 $(document).tooltip();

 $("textarea").focusin(function(){
	$(document).tooltip('disable');
 });
$("textarea").focusout(function(){
	$(document).tooltip('enable');
 });

 $("input").focusin(function(){
	$(document).tooltip('disable');
 });
 $("input").focusout(function(){
	$(document).tooltip('enable');
 });

 //    Button-based Ajax     //
 $(document).on("click", ".upvoteButton", function (){
   var pid = $(this).attr("pid");
   var model = $(this).attr("model");
   $.get("/vote/", {direction: "+", pid:pid, model:model}, function(response) {
    alert(response) //Do something better...     
   });
 })
 $(document).on("click", ".downvoteButton", function (){
   var pid = $(this).attr("pid");
   var model = $(this).attr("model");
   $.get("/vote/", {direction: "-", pid:pid, model:model}, function(response) {
    alert(response) //Do something better...     
   });
 })


 $(document).on("click", ".addListInputButton", function (){
  var container = $(".listInputcontainer:last");
  $(container).clone().insertAfter($(container))
  setAutoComplete($(".autocomplete"))
  $(".listInputContainer:last").find("input[name=\"related[]\"]").val("");
  $(this).remove()
 });

 $(document).on("mouseenter", ".listInputContainer", function(){
   if (!$(".addListInputButton").length) {
    $(this).append("<div class=\"addListInputButton\" title=\""
     + "Add another related node.\">+</div>");
   }
  })
 
 $(document).on("mouseleave", ".listInputContainer", function(){
   $(".addListInputButton").remove();
 });



$('.kwicks').kwicks({
	maxSize: "21%",
        autoResize: true,
        spacing: 0,
	duration: 200,
        behavior: 'menu',
	interactive: false,	
    });
//$('.kwicks').kwicks('expand', 0);

$('#userContainer li ul').hide().removeClass('fallback');
$('userContainer li').hover(
    function () {
        $('ul', this).stop().slideDown(100);
    },
    function () {
        $('ul', this).stop().slideUp(100);
    }
);
});


