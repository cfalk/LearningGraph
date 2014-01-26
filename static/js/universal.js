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

 function format_rating(nodeStats, score){ 
  if (score>0){
   $(this).addClass("goodColorText");
   $(this).removeClass("badColorText");
   $(this).removeClass("neutralColorText");
   $(this).html("+"+String(score+1));
  } else if (score<0){
   $(this).addClass("badColorText");
   $(this).removeClass("goodColorText");
   $(this).removeClass("neutralColorText");
   $(this).html("-"+String(score-1));
  } else {
   $(this).addClass("neutralColorText");
   $(this).removeClass("goodColorText");
   $(this).removeClass("badColorText");
   $(this).html("0");
  }
 }

 //    Button-based Ajax     //
 $(document).on("click", ".upvoteButton", function (){
   var pid = $(this).attr("pid");
   var model = $(this).attr("model");
   $.get("/vote/", {direction: "+", pid:pid, model:model}, function(response) {
    if (response!=0){
     showRibbon(response, badColor, "body")
    } else {
     score = parseInt($("#nodeStats span").html());
     format_rating($("#nodeStats span", score));
     showRibbon("Thanks!", goodColor, "body");
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
     showRibbon("Thanks!", goodColor, "body")
    }
   });
 })


 $(document).on("click", ".addListInputButton", function (){
  var container = $(".listInputcontainer:last").closest("li");
  if ($(container).find(".listInput").val()){
   $(container).clone().insertAfter($(container))
   setAutoComplete($(".autocomplete"))
   $(".listInputContainer:last").find(".listInput").val("");
   $(this).remove()
   
   $(".sortable").sortable({
    stop: function () {
     // enable text select on inputs
     $(".sortable").find("input")
      .bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
       e.stopImmediatePropagation();
     });
   }
   }).disableSelection();

   // enable text select on inputs
   $(".sortable").find("input")
    .bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
    e.stopImmediatePropagation();
   });

  }
 });

 $(document).on("click", ".addListInputButton2", function (){
  var container = $(".listInputcontainer2:last").closest("li");
  if ($(container).find(".listInput").val()){
   $(container).clone().insertAfter($(container))
   setAutoComplete($(".autocomplete"))
   $(".listInputContainer2:last").find(".listInput").val("");
   $(this).remove()

  }
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


 $(document).on("mouseenter", ".listInputContainer2", function(){
   if (!$(".addListInputButton").length) {
    $(this).append("<div class=\"addListInputButton2\" title=\""
     + "Add another related node.\">+</div>");
   }
  })
 
 $(document).on("mouseleave", ".listInputContainer2", function(){
   $(".addListInputButton2").remove();
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

function markdown(content) {
   var converter = Markdown.getSanitizingConverter();
   return converter.makeHtml(content);
}


/*       Node Editing        */

$(document).on("click", ".editButton", function (){
 var oldContent = $("#rawContent").html();
 $("#nodeContent").replaceWith("<textarea id=\"nodeContent\" name=\"content\" "
   +"oldContent=\""+oldContent+"\">"+oldContent+"</textarea>");
 $(".saveButton").show()
 $(".cancelButton").show()
 $(this).hide()
});

$(document).on("click", ".cancelButton", function (){
 var oldContent = $("#nodeContent").attr("oldContent");
 $("#nodeContent").replaceWith("<div id=\"nodeContent\">"+markdown(oldContent)+"</div>");
 $(".editButton").show()
 $(".saveButton").hide()
 $(this).hide()
});

$(document).on("click", ".saveButton", function (){
 var newContent = $("#nodeContent").val();
 $("#rawContent").html(newContent);
 $.ajax({
  type:"GET", 
  url: "/edit_node/", 
  data: { 
     name: $("#node").attr("pid"), 
     content: newContent}}).done(function(msg) {
       if (msg!=0){
        showRibbon(msg, badColor, "body");
       } else {
        showRibbon("Saved!", goodColor, "body")
        $(".saveButton").hide()
        $(".cancelButton").hide()
        $(".editButton").show()
        $("#nodeContent").replaceWith("<div id=\"nodeContent\">"+markdown(newContent)+"</div>");
       }
     });

})

$(".sortable").sortable({
  stop: function () {
    // enable text select on inputs
    $(".sortable").find("input")
     .bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
      e.stopImmediatePropagation();
    });
  }
}).disableSelection();

// enable text select on inputs
$(".sortable").find("input")
 .bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
  e.stopImmediatePropagation();
});


});


