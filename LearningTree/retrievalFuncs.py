from models import *
from django.db.models import Q

# # # # # # # # # Edge # # # # # # # # # # # # # # # # # # 
def get_node_edges(node):
 return Edge.objects.filter(Q(node1=node)|Q(node2=node))

def get_edges(n1, n2):
 return Edge.objects.filter(Q(node1=n1, node2=n2)|Q(node1=n2, node2=n1))

def get_all_edges():
 return Edge.objects.all()

# # # # # # # # # Node # # # # # # # # # # # # # # # # # # 
def get_node(name):
 return Node.objects.filter(name=name)[0]

def get_user_nodes(user):
 return Node.objects.filter(user=user)

def get_user_careers(user):
 return Career.objects.filter(user=user)

# # # # # # # # # # Link # # # # # # # # # # # # # # # # # 
def get_link(link):
 return Link.objects.filter(url=name)[0]

def get_career(name):
 return Career.objects.filter(name=name)[0]

def get_careernodemap_by_career(career):
 return CareerNodeMap.objects.filter(career=career)

def get_careernodemap_by_node(node):
 return CareerNodeMap.objects.filter(node=node)

def get_career_nodes(career):
 return get_careernodemap_by_career(career=career).values("node")

def get_node_careers(node):
 return get_careernodemap_by_career(node=node).values("career")
