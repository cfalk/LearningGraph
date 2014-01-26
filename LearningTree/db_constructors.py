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
  return e
 except Exception as e:
  print "Edge construct failed: {}".format(e)
  raise Exception("Edge construction failed.")

def new_careernodemap(node, career, user):
 try:
  node = get_node(node)
  career = get_career(career)
  cnm = CareerNodeMap()
  cnm.node = node
  cnm.career = career
  cnm.user = user
  cnm.save()
  return cnm
 except Exception as e:
  print e
  raise Exception("CareerNodeMap construction failed")

#Create a new edge and apply it to a career.
def new_careeredgemap(node1, node2, career, user):
 try:
  #Variable Setup
  cem = CareerEdgeMap(user=user, career=career)
  n1 = get_node(node1)
  n2 = get_node(node2)

  #Either get the edge or make a new edge.
  try:
   e = get_edges(n1,n2)[0]
  except:
   #Create the Edge
   e = new_edge(n1, n2)
  assert e #Make sure an edge was collected

  #Make a CareerNodeObject for each node.
  new_careernodemap(n1, career, user)
  new_careernodemap(n2, career, user)
  
  cem.edge = e
  cem.save()
  return cem
 except Exception as e:
  print e
  raise Exception("CareerNodeMap construction failed")



