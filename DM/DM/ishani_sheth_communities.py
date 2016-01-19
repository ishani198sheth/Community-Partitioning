import networkx as nx
import community as com
import sys
import operator
import matplotlib.pyplot as plt
import itertools
import random
random.seed(0)
#reading what file is to be considered as input from the terminal
input_file = sys.argv[1]
input_datafile = open(input_file, "r")
image_file= sys.argv[2]
#initializing an empty list of nodes and edges
list_nodes=[]
list_edges=[]

#creating an empty graph
graph= nx.Graph()

#reading the input file and adding the nodes and edges to its respective list
for line in input_datafile:
    data= line.strip().split()
    if int(data[0]) not in list_nodes:
        list_nodes.append(int(data[0]))
    if int(data[1]) not in list_nodes:
        list_nodes.append(int(data[1]))
    edge=(int(data[0]),int(data[1]))
    list_edges.append(edge)
list_nodes.sort()

#adding the nodes and edges to the graph from the input file
graph.add_nodes_from(list_nodes)
graph.add_edges_from(list_edges)

#nx.draw(graph)
#plt.show()
def random_color():
    r=hex(random.randint(0,255)).split('x')[1]
    g=hex(random.randint(0,255)).split('x')[1]
    b=hex(random.randint(0,255)).split('x')[1]
    color='#'+r+g+b
    return color
#calculating betweeness and removing edges with max betweenness
def betweeness_calculation(graph):
    betweeness = nx.edge_betweenness(graph, k=None, normalized=False, weight=None, seed=None)
    graph.remove_edge(*(max(betweeness.iteritems(), key=operator.itemgetter(1))[0]))
    return graph

#for calculating the partition of the graph
#partition returns a dictionary with nodes in a community as key and community name as value
#eg 2:0 where 2 is the node in community 0
def partition(graph):
    partition={}
    summation_edges=0
    
    graphs = list(nx.connected_component_subgraphs(graph))
    
    for i in range(len(graphs)):
        summation_edges=summation_edges+len(list(graphs[i].edges())) #sum of total edges in the graph
        community=list(graphs[i].nodes())
        for nodes in community:
            partition[nodes]=i
    
    return partition,summation_edges

total_edges= graph.number_of_edges()
graph_modified=betweeness_calculation(graph)
modularity_partition_mapping=[]

while(total_edges>0):

    #calculate partition on graph_modified
    partitions=partition(graph_modified)
    total_edges=partitions[1]
    if total_edges==0:
        break
    #calculating modularity
    modularity=com.modularity(partitions[0],graph)
    
    #calculate betweenness for a graph
    modularity_partition_mapping.append([modularity,partitions[0]])
    graph_modified1=betweeness_calculation(graph_modified)
    
#appending all modularities to list and getting the max modularity out of it
total_modularities=[]
for elements in modularity_partition_mapping:
    total_modularities.append(elements[0])

max_modularity=max(total_modularities)

#getting the partition associated with maximum modularity
max_partition={}
for element in modularity_partition_mapping:
    if element[0]==max_modularity:
        max_partition=element[1]
#print max_partition

#getting all the communities from the partition in a dictionary with communities as key and list of elements in it as values
v = {}
for key, value in sorted(max_partition.iteritems()):
    v.setdefault(value, []).append(key)

# printing all the communities
for items in v:
    print v[items]

#creating the final graph

final_graph=nx.Graph()
for items in v:
     #edges=list(itertools.combinations(v[items],2))
     final_graph.add_nodes_from(v[items])
     final_graph.add_edges_from(list_edges)
pos=nx.spring_layout(final_graph) 

for items in v:
    #edges_colored=list(itertools.combinations(v[items],2))
    nx.draw_networkx_nodes(final_graph,pos,
                       nodelist=v[items],
                       node_color=random_color(),
                       node_size=500,
                       alpha=1)
    nx.draw_networkx_edges(final_graph,pos,
                       edgelist=list_edges,
                       width=1,alpha=1,edge_color='k')   
#nx.draw(final_graph)
labels={}
for i in list_nodes:
    labels[i]=i
nx.draw_networkx_labels(final_graph,pos,labels,font_size=12)
plt.axis('off')
plt.savefig(image_file)
plt.show()


        
