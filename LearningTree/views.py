from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import *
from django.template import RequestContext

from models import *
from forms import *
from db_constructors import *
from retrievalFuncs import *

def home(request):
 return render(request, "index.html")

def node(request):
 return render(request, "node.html")

def node_form(request):
 u = request.user
 
 if u.is_authenticated() and request.method=="POST":
  node= Node()
  node.user = u
  form = NodeForm(request.POST, instance=node) 

  if form.is_valid():
   form.save()
  return HttpResponse("Node created!")
 else:
  form = NodeForm() 

 return render(request,"node_form.html", {"form":form})
 
def login(request):
 if request.user.is_authenticated():
  return redirect('/index/')
 return render_to_response('login.html', {}, RequestContext(request))

def user_nodes(request):
 u= request.user
 if u.is_authenticated():
  nodes = get_user_nodes(u) 
 else:
  nodes = None
 return render(request, "user_nodes.html", {"nodes": nodes})

