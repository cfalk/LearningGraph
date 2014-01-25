from django import forms
from models import *

class NodeForm(forms.ModelForm):
 content = forms.CharField(widget=forms.Textarea)

 class Meta:
  model = Node
  #Put the fields in order.
  fields = ["name","content"]

