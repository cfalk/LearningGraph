from models import *

def new_node(user, name, content, related): #related is a list of nodes that will be connected to this node by edges
 n = Node()
 n.name = name
 n.user = user
 n.content = content
 n.save()
 for node in related:
  e = Edge(node1=n, node2=node)
  e.save()

