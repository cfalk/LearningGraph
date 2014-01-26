from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import *
from django.template import RequestContext

import json

from models import *
from forms import *
from db_constructors import *
from retrievalFuncs import *

import random #TODO / Note from Casey: This was acting up for some reason.

def info_page(request, page):
 return render(request, "info_page_global.html", {"template":page})

def edit_node(request):
 try:
  #Variable Setup
  u = request.user
  n = Node.objects.get(id=request.GET["name"])

  #Make sure the user owns the node.
  if (not u.is_authenticated()):# or n.user != u):
   return HttpResponse("You don't have access to edit this Node.")

  n.content = request.GET["content"]
  parse_links(request.GET["content"])
  n.save()
  return HttpResponse(0)
 except Exception as e:
  print "ERROR: {}".format(e)
  return HttpResponse("Edit failed!") 

def format_rating(rating):
 print rating
 if rating > 0:
  rating = "<span class=\"goodColorText\">+{}</span>".format(rating)
 elif rating < 0:
  rating = "<span class=\"badColorText\">{}</span>".format(rating)
 else:
  rating = "<span class=\"neutralColorText\">0</span>"
 print rating
 return rating

def node(request):
 try:
  name= request.GET["node"]
  n = get_node(request.GET["node"])
  career = request.GET.get("career")
  rating = format_rating(n.good-n.bad)
  if career:
   career = get_career(career)
 except Exception as e:
  print e
  n = None
  career = None
  rating = 0
 return render(request, "info_page_global.html", {"template":"node", "node":n, "rating":rating, "career":career})

def career(request):
 try:
  name = request.GET["career"]
  career = get_career(name)
  careernodemap = get_careernodemap_by_career(career)
 except Exception as e:
  print e
  career = None
  careernodemap = None
 return render(request, "info_page_global.html", {"template":"career", "career":career,"careernodemap":careernodemap})

def random_node(request):
 random_idx = random.randint(0, Node.objects.count() - 1)
 node = Node.objects.all()[random_idx]
 edges = get_node_edges(node)
 rating = format_rating(node.good-node.bad)
 return render(request, "info_page_global.html", {"template":"node", "node":node, "edges":edges, "rating":rating})


def career_form(request):
 u = request.user
 fatal_message = ""
 if u.is_authenticated() and request.method=="POST":
  career = Career()
  career.user = u

  #Insanity Checking
  try:
   path = request.POST.getlist("path[]")
   assert path[0]
   try:
    career.start_node = get_node(path[0])
   except:
    fatal_message = "Start node not found."
  except:
   fatal_message = "Please specify a skill path."

  form = CareerForm(request.POST, instance=career) 
  if not fatal_message and form.is_valid(): 
   form.save() #Make the Career.
   try:
    print "LENGTH: {}".format(len(path))
    if len(path)==1: #If only one element exists in the career path...
     new_careernodemap(path[0], career, u)
    else:
     for i in xrange(len(path)-1):
      new_careeredgemap(path[i], path[i+1], career, u)

    return render(request, "info_page_global.html", {"template":"career_form", "form":form, "addedCareer":career})
   except Exception as e:
    print e
    career.delete()
    fatal_message = "Could not create Career!"
 else:
  form = CareerForm() 
 return render(request, "info_page_global.html", {"template":"career_form", "form":form, "fatalMessage":fatal_message})

def node_form(request):
 u = request.user
 
 if u.is_authenticated() and request.method=="POST":
  n= Node()
  n.user = u
  form = NodeForm(request.POST, instance=n) 
  if form.is_valid():
   #Variable Setup
   form.save()
   parse_links(request.POST["content"])
   #Make the edges if edges are supplied.
   if request.POST.get("related[]"):
    related_nodes = request.POST.getlist("related[]")
    for name in related_nodes:
     try:
      new_edge(n.name, name)
     except Exception as e:
      pass
   return render(request, "info_page_global.html", {"template":"node_form", "form":form, "addedNode":n})
 else:
  form = NodeForm() 
 return render(request, "info_page_global.html", {"template":"node_form", "form":form})
 
def login(request):
 if request.user.is_authenticated():
  return redirect('/explore/')
 return render_to_response('login.html', {}, RequestContext(request))

def logout_view(request):
 logout(request)
 return redirect('/explore/')

def user_nodes(request):
 u= request.user
 if u.is_authenticated():
  nodes = get_user_nodes(u) 
 else:
  nodes = None
 return render(request, "info_page_global.html", {"template":"user_nodes", "nodes":nodes})

def edge_form(request):
 u = request.user
 fatal_message = ""
 if u.is_authenticated() and request.method=="POST":
  #Variable Setup
  try:
   node1 = request.POST["node1"]
   node2 = request.POST["node2"]
   n1 = get_node(node1)
   n2 = get_node(node2)
  except:
   fatal_message = "One of the nodes could not be found."

  if not fatal_message:
   #Check that the edge does not already exist. 
   assert not get_edges(n1, n2).exists()
 
   #Add the Edge.
   try:
    new_edge(n1, n2) 
   except:
    fatal_message="Connection could not be made."
 
   if not fatal_message:
    return render(request, "info_page_global.html", {"template":"edge_form", "success":True})
 return render(request, "info_page_global.html", {"template":"edge_form","fatalMessage":fatal_message})

def user_careers(request):
  u = request.user
  if u.is_authenticated():
   careers = get_user_careers(u)
  else:
   careers = None
  return render(request, "info_page_global.html", {"template": "user_careers", "careers": careers})


# # # # # # # # # # # # # AJAX Requests # # # # # # # # # # 
def get_node_names(request):
 node_names = [unicode(entry.name) for entry in Node.objects.all()]
 return HttpResponse(json.dumps(node_names), content_type="application/json")

def get_career_names(request):
 career_names = [unicode(entry.name) for entry in Career.objects.all()]
 return HttpResponse(json.dumps(career_names), content_type="application/json")

def get_edge_pairs(request):
 try:
  pid = request.GET.get("pid")
  career = request.GET.get("career")

  if pid:
   n = Node.objects.get(id=pid)
   dirty_edges = get_node_edges(n)
  else:
   dirty_edges = get_all_edges()

  if career:
   print "_____________________________________________FILTERED"
   dirty_data = dirty_data.filter(careeredgemap__career=get_career(career))
   print "_____________________________________________FILTERED"

  edge_list = [[unicode(edge.node1), unicode(edge.node2)] for edge in dirty_edges]
  return HttpResponse(json.dumps(edge_list), content_type="application/json")
 except Exception as e:
  print e

def vote(request):
 u = request.user
 if u.is_authenticated():
  #Variable Setup:
  direction = request.GET["direction"] 
  pid  = request.GET["pid"] 
  model  = request.GET["model"] 

  if model=="node": #TODO: Expand to other models.
   data = Node.objects.get(id=pid)
  else:
   return HttpResponse("Illegal option.")


  if direction=="+":
   data.good += 1
  elif direction=="-":
   data.bad += 1
  else:
   return HttpResponse("Illegal option.")

  data.save()
  return HttpResponse(0)
 else:
  return HttpResponse("Please log in to vote.") 


def parse_links(raw_content):
 import re
 matches = re.findall('\((.*?)\)', raw_content)
 for match in matches:
  try:
   l = Link(url=match)
   l.save()
  except Exception:
   pass 
