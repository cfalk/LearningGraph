from django import forms
from models import *

class NodeForm(forms.ModelForm):
 content = forms.CharField(widget=forms.Textarea(attrs={'title': 'Add Description and Links.'}))
 class Meta:
  model = Node
  #Put the fields in order.
  fields = ["name","content"]


class CareerForm(forms.ModelForm):
 description = forms.CharField(widget=forms.Textarea)
 class Meta:
  model = Career
  fields = ["name", "description"]
