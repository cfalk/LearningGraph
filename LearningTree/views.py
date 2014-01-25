from django.http import HttpResponse
from django.shortcuts import render

from models import *
from db_constructors import *

def home(request):
 return render(request, "index.html")

def node(request):
 return render(request, "node.html")
