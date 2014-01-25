from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import *

from models import *
from forms import *
from db_constructors import *


def home(request):
 return render(request, "index.html")

def node(request):
 return render(request, "node.html")

def node_form(request):
 u = request.user

 if u.is_authenticated() and request.method=="POST":
  form = NodeForm(request.POST) 
  if form.is_valid():
   form.user = u
   form.save()
 else:
  form = NodeForm() 

 return render(request,"node_form.html", {"form":form})
