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
  form = CareerForm(request.POST, instance=node) 

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
  node= Node()
  node.user = u
  form = NodeForm(request.POST, instance=node) 

  if form.is_valid():
   try:
    related = request.POST.get_list("related[]")
    for name in related_nodes:
     try:
      new_edge(node.name, name)
     except Exception as e:
      print e     
      pass
   except:
    pass
   form.save()
   return HttpResponse(0)
  else:
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

def get_node_names(request):
 try:
  node_names = [unicode(entry.name) for entry in Node.objects.all()]
  return HttpResponse(json.dumps(node_names), content_type="application/json")
 except Exception as e:
  print e

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

#def graph(request):
# return render(request, 
