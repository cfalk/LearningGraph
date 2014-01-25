from models import *

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


