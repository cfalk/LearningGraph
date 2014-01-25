from django.http import HttpResponse
from django.shortcuts import render

from models import *

def home(request):
 return render(request, "index.html")
