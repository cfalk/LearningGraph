function loadGraph(title){
var links = [];
var link;
var obj = {};
var width=700;
var height = 600;
var career_appendage = "";
var career = document.getElementById("career");

if(career){
	var carText = career.innerHTML;
	career_appendage="&?career="+carText;
}

if(!title){
	url_appendage="";
} else {
	url_appendage="?pid="+title;
	height=300;
}

$.getJSON("/get_edges/"+url_appendage+career_appendage, function(data) {
 $.each(data, function(i, v){
	links.push({
       		source : v[0],
       		target : v[1]
    	 })	
   });
 

var nodes = [];
// Compute the distinct nodes from the links.
links.forEach(function(link) {
link.source = nodes[link.source] || 
(nodes[link.source] = {name: link.source});
link.target = nodes[link.target] || 
(nodes[link.target] = {name: link.target});
link.value = +link.value;
});

var color = d3.scale.category20();

var force = d3.layout.force() 
.nodes(d3.values(nodes)) 
.links(links) 
.size([width, height]) 
.linkDistance(120) 
.charge(-300) 
.on("tick", tick) 
.start(); 

var svg = d3.select("div.container").append("svg") 
.attr("width", "90%") 
.attr("height", height);

var link = svg.selectAll(".link") 
.data(force.links()) 
.enter().append("line") 
.attr("class", "link"); 

var node = svg.selectAll(".node") 
.data(force.nodes()) 
.enter().append("g") 
.attr("class", "node") 
.on("mouseover", mouseover) 
.on("mouseout", mouseout) 
.on("click", click)
.on("dblclick", dblclick)
.call(force.drag); 

node.append("circle") 
.attr("r", 8) // function(d) { return d.views; })
.style("fill", function(d) { return color(d.value); });

node.append("text") 
.attr("x", 12) 
.attr("dy", ".35em") 
.style("fill", "steelblue")
.text(function(d) { return d.name; }); 



function tick() { 
link 
.attr("x1", function(d) { return d.source.x; }) 
.attr("y1", function(d) { return d.source.y; }) 
.attr("x2", function(d) { return d.target.x; }) 
.attr("y2", function(d) { return d.target.y; }); 

node 
.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; }); 
} 

function mouseover() { 
d3.select(this).select("circle").transition() 
.duration(750) 
.attr("r", 16); 
} 

function mouseout() { 
d3.select(this).select("circle").transition() 
.duration(750) 
.attr("r", 8); 
} 
// action to take on mouse click
function click() {
d3.select(this).select("text").transition()
.duration(750)
.attr("x", 22)
.style("stroke-width", ".5px")
.style("fill", "#E34A33")
.style("font", "20px serif");
d3.select(this).select("circle").transition()
.duration(750)
.style("fill", "#E34A33")
.attr("r", 16)
}

// action to take on mouse double click
function dblclick() {

var text = d3.select(this).text();

var url ="/node/?node="+encodeURIComponent(text);

window.location=url;
}
})
}
