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

 $(document).on("submit", "#nodeForm", function(event) {
  $(".errorlist").remove() // Remove any errors that exist.
  form = $(this);
  form_data = $(this).serialize()
  $.post($(form).attr("action"), form_data, function(response) {
   if (response!="0"){
    $("#nodeForm").html(response)
    setAutoComplete(".autocomplete")
   } else {
    $("form").find("input[type=text]").val("");
    $("form").find("textarea").val("");
    showRibbon("Leaf added!", goodColor, "body"); 
   }
  });
  //Don't allow the original form to submit.
  event.stopPropagation();
  return false;
 })

$(document).on("submit", "#careerForm", function(event) {
  $(".errorlist").remove() // Remove any errors that exist.
  form = $(this);
  form_data = $(this).serialize()
  $.post($(form).attr("action"), form_data, function(response) {
   if (response!="0"){
    $("#careerForm").html(response)
   } else {
    $("form").find("input[type=text]").val("");
    showRibbon("Career added!", goodColor, "body");
   }
  });
  //Don't allow the original form to submit.
  event.stopPropagation();
  return false;
 })


 $(document).on("click", ".addListInputButton", function (){
  var container = $(this).closest(".listInputcontainer");
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

});


