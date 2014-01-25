from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

class NodeForm(forms.Form):
	name = forms.CharField(max_length=45)
	user = forms.CharField()
	content = forms.CharField()
	related = forms.CharField()

def add_node(request):
	if request.method == 'POST'
		form = NodeForm(request.POST)
		if form.is_valid():
			#return HttpResponseRedirect() NEEDS REDIRECT
	else:
		form = NodeForm()
	return render(request, '', {'form':form})





def new_node(name, user, content, related): #related is a list of nodes that will be connected to this node by edges
	n = Node()
	n.name = name
	n.user = user
	n.content = content
	n.save()
	for node in related:
		e = Edge()
		e.node1 = n
		e.node2 = node
		e.save()

