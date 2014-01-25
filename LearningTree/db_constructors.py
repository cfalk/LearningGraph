from models import *
from django.db.models import Q

def new_node(user, name, content, related): #related is a list of nodes that will be connected to this node by edges
 n = Node()
 n.name = name
 n.user = user
 n.content = content
 n.save()
 for node in related:
  e = Edge(node1=n, node2=node)
  e.save()


def new_edge(name1, name2):
 try:
  #Get the Node objects.
  n1 = Node.objects.filter(name=name1)[0]
  n2 = Node.objects.filter(name=name2)[0]

  #Insanity Checking:
   #No Node should be linked to itself directly.
  assert node_name1 != node_name2
   #No Edge should already exist.
  assert not Edge.objects.filter(node1=n1, node2=n2).exists()
  assert not Edge.objects.filter(node2=n2, node1=n1).exists()

  #Save the new node.
  e = Edge(node1=n1, node2=n2)
  e.save()
 except Exception as e:
  print "Edge construct failed: {}".format(e)

