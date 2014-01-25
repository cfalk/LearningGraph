from retrievalFuncs import *

def new_node(user, name, content, related): #related is a list of nodes that will be connected to this node by edges
 n = Node()
 n.name = name
 n.user = user
 n.content = content
 n.save()
 for node in related:
  e = Edge(node1=n, node2=node)
  e.save()


#Create a new edge between two Nodes (input by name) or fail.
def new_edge(name1, name2):
 try:
  #Get the Node objects.
  n1 = get_node(name1)
  n2 = get_node(name2)

  #Insanity Checking:
   #No Node should be linked to itself directly.
  assert name1 != name2 != None 
   #No Edge should already exist.
  assert not get_edges(n1, n2).exists()

  #Save the new node.
  e = Edge(node1=n1, node2=n2)
  e.save()
 except Exception as e:
  print "Edge construct failed: {}".format(e)

