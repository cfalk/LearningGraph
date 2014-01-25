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

def node(request):
 try:
  name = request.GET["node"]
  node = get_node(name)
  edges = get_node_edges(node)
 except:
  node = None
  edges = None
 return render(request, "info_page_global.html", {"template":"node", "node":node, "edges":edges})

def random(request):
 node = random.choice(Node.objects.all())
 edges = get_node_edges(node)
 return render(request, "node.html", {"node": node, "edges":edges})
 

def career_form(request):
 u = request.user

 if u.is_authenticated() and request.method=="POST":
  career = Career()
  career.user = u
  career.start_node = get_node(request.POST.get("start_node"))
  form = CareerForm(request.POST, instance=career) 

  if form.is_valid():
   form.save()
   return HttpResponse(0)
  else:
   return render(request, "career_form.html", {"form":form})
 else:
  form = CareerForm() 
 return render(request, "info_page_global.html", {"template":"career_form_page", "form":form})

def node_form(request):
 u = request.user
 
 if u.is_authenticated() and request.method=="POST":
  try: 
   node= Node()
   node.user = u
   form = NodeForm(request.POST, instance=node) 
   form.save()
   assert form.is_valid()
   
   #Make the edges if edges are supplied.
   if request.POST.get("related[]"):
    related_nodes = request.POST.getlist("related[]")
    for name in related_nodes:
     try:
      new_edge(node.name, name)
     except Exception as e:
      pass
   return HttpResponse(0)
  except:
   return render(request, "node_form.html", {"form":form})
 else:
  form = NodeForm() 
 return render(request, "info_page_global.html", {"template":"node_form_page", "form":form})
 
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
 try:
  node_names = [unicode(entry.name) for entry in Node.objects.all()]
  return HttpResponse(json.dumps(node_names), content_type="application/json")
 except Exception as e:
  print e

def get_edge_pairs(request):
 try:
  edges = [[unicode(edge.node1), unicode(edge.node2)] for edge in get_all_edges()]
  return HttpResponse(json.dumps(edges), content_type="application/json")
 except:
  pass



