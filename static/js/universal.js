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
 // Enable jQuery Auto-Complete
 var career_nodes;
 function setCareerAutoComplete(object){
  if (career_nodes !== undefined) {
    $(object).autocomplete({
     source: career_nodes
    });
  } else {
   $.getJSON("/get_career_names/", function(data) {
    career_nodes = data;
    $(object).autocomplete({
     source: data
    });
   })
  }
 }
 //Right off the bat, load the autocomplete for 


 setAutoComplete(".autocomplete")
 setCareerAutoComplete(".autocomplete_career")

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
    if (response!=0){
     showRibbon(response, badColor, "body")
    } else {
     $("#nodeStats").html(parseInt($("#nodeStats").html())+1)
     showRibbon("Vote counted!", goodColor, "body")
    }
   });
 })
 $(document).on("click", ".downvoteButton", function (){
   var pid = $(this).attr("pid");
   var model = $(this).attr("model");
   $.get("/vote/", {direction: "-", pid:pid, model:model}, function(response) {
    if (response!=0){
     showRibbon(response, badColor, "body")
    } else {
     $("#nodeStats").html(parseInt($("#nodeStats").html())-1)
     showRibbon("Vote counted!", goodColor, "body")
    }
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


/*       Node Editing        */

$(document).on("click", ".editButton", function (){
 oldContent = $("#nodeContent").html();
 $("#nodeContent").replaceWith("<textarea id=\"nodeContent\" name=\"content\" "
   +"oldContent=\""+oldContent+"\">"+oldContent+"</textarea>");
 $(".sideButton").show()
 $(".cancelButton").show()
 $(this).hide()
});

$(document).on("click", ".cancelButton", function (){
 oldContent = $("#nodeContent").attr("oldContent");
 $("#nodeContent").replaceWith("<div id=\"nodeContent\">"+oldContent+"</div>");
 $(".editButton").show()
 $(".saveButton").hide()
 $(this).hide()
});

$(document).on("click", ".saveButton", function (){
 oldContent = $("#nodeContent").html();

 $.ajax({
  type:"GET", 
  url: "/edit_node/", 
  data: { 
     name: $("#node").attr("pid"), 
     content: oldContent}}).done(function(msg) {
       if (msg!=0){
        showRibbon("Failed!", goodColor, "body");
        $(".cancelButton").trigger("click");
       } else {
        showRibbon("Saved!", goodColor, "body")
        oldContent = $("#nodeContent").attr("oldContent");
       }
     });

})

});


