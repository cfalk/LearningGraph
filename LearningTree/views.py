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
  assert u.is_authenticated() and n.user == u

  n.content = request.GET["content"]
  n.save()
  return HttpResponse(0)
 except Exception as e:
  print e
  return HttpResponse("Edit failed!") 

def node(request):
 try:
  name = request.GET["node"]
  node = get_node(name)
  edges = get_node_edges(node)
 except:
  node = None
  edges = None
 return render(request, "info_page_global.html", {"template":"node", "node":node, "edges":edges})

def career(request):
 try:
  name = request.GET["career"]
  career = get_career(name)
 except:
  career = None
 print career
 return render(request, "info_page_global.html", {"template":"career", "career":career})

def random_node(request):
 random_idx = random.randint(0, Node.objects.count() - 1)
 node = Node.objects.all()[random_idx]
 edges = get_node_edges(node)
 return render(request, "info_page_global.html", {"template":"node", "node": node, "edge": edges})
 

def career_form(request):
 u = request.user
 if u.is_authenticated() and request.method=="POST":
  career = Career()
  career.user = u
  career.start_node = get_node(request.POST.get("start_node"))
  form = CareerForm(request.POST, instance=career) 

  if form.is_valid():
   form.save()
   return render(request, "info_page_global.html", {"template":"career_form", "form":form, "addedCareer":career})
 else:
  form = CareerForm() 
 return render(request, "info_page_global.html", {"template":"career_form", "form":form})

def node_form(request):
 u = request.user
 
 if u.is_authenticated() and request.method=="POST":
  node= Node()
  node.user = u
  form = NodeForm(request.POST, instance=node) 
  if form.is_valid():
   #Variable Setup
   form.save()

   #Make the edges if edges are supplied.
   if request.POST.get("related[]"):
    related_nodes = request.POST.getlist("related[]")
    for name in related_nodes:
     try:
      new_edge(node.name, name)
     except Exception as e:
      pass
   return render(request, "info_page_global.html", {"template":"node_form", "form":form, "addedNode":node})
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

def add_career(request):
 u = request.user
 if u.is_authenticated() and request.method=="POST":
  career = Career()
  form = CareerForm(request.POST, instance=career)
  if form.is_valid():
   form.save()
   return HttpResponse(0)
 else:
  form = CareerForm()
 return render(request, "info_page_global.html", {"template":"career_form", "form":form}) 



# # # # # # # # # # # # # AJAX Requests # # # # # # # # # # 
def get_node_names(request):
 node_names = [unicode(entry.name) for entry in Node.objects.all()]
 return HttpResponse(json.dumps(node_names), content_type="application/json")

def get_edge_pairs(request):
 try:
  name = request.GET.get("node")
  if name:
   n = get_node(n)
   dirty_edges = get_node_edges(node)
  else:
   dirty_edges = get_all_edges()

  edge_list = [[unicode(edge.node1), unicode(edge.node2)] for edge in get_all_edges()]
  return HttpResponse(json.dumps(edge_list), content_type="application/json")
 except Exception as e:
  print e

