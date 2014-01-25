from models import *
from django.db.models import Q

def get_user_nodes(user):
 return Node.objects.filter(user=user)

def get_node_edges(node):
 return Edge.objects.filter(Q(node1=node)|Q(node2=node))

def get_node(name):
 return Node.objects.filter(name=name)[0]

def get_edge(n1, n2):
 return Edge.objects.filter(Q(node1=n1, node2=n2)|Q(node1=n2, node2=n1))
