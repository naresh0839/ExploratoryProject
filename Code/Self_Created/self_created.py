import igraph
from igraph import *
import random
import math
import time

start_time = time.time()

graph = Graph.Read_GML("football.gml")
#graph = igraph.read("netsience.net", format = "pajek")
#graph = Graph.Read_GML("football.gml")

Graph = graph.get_adjacency()		# future testing set

N = len(Graph[0]) # number of nodes in graph

futureGraph = []
currentGraph = []

for i in range(0, N):
	tmp = []
	futureGraph.append(tmp)
	currentGraph.append(tmp)

edge = 0 	# number of edges present in futureGraph
edges = []	# list of edges present 

unconnected = [] # edges which are not in either currentGraph or FutureGraph
missing = [] # edges which are constructed between training and testing data

for i in range(0, N):
	for j in range(i + 1, N):
		if (Graph[i][j]):
			futureGraph[i].append(j)
			futureGraph[j].append(i)
			currentGraph[i].append(j)
			currentGraph[j].append(i)
			edges.append((i, j))
			edge += 1
		else:
			unconnected.append((i, j))
			
print("Number of edges ::"+str(edge))
print("Number of Nodes ::"+str(N))

delete = int(edge / 10)

for i in range(0, delete):
	idx = random.randrange(0, len(edges))
	it = edges[idx]
	edges.remove(it)
	missing.append(it)
	currentGraph[it[0]].remove(it[1])
	currentGraph[it[1]].remove(it[0])

score1 = {}
score2 = {}
score3 = {}
for x in range(0, N):
	temp = []
	for y in range(x + 1, N):
		Score1 = 0
		Score2 = 0
		Score3 = 0
		score1[(x,y)]= 0
		score2[(x,y)]= 0
		score3[(x,y)]= 0
		for i in range(0, N):
			if (i in currentGraph[x]) and (i in currentGraph[y]):
				Score2 += 1
				Score3 += 1
				if len(currentGraph[i]) > 1:
					Score1 += 1 / math.log(len(currentGraph[i]))
		if len(currentGraph[x])>0 and len(currentGraph[y])>0:
			Score3 = Score3 / math.sqrt(len(currentGraph[x]) * len(currentGraph[y]))
		score1[(x,y)] = Score1
		score2[(x,y)] = Score2
		score3[(x,y)] = Score3

total1 = len(missing) * len(unconnected)
# total is the number of times that we randomly pick a pair of links from missing links set and unconnected links set
n11 = 0
n12 = 0
n21 = 0
n22 = 0
n31 = 0
n32 = 0

for x in unconnected:
	score_un = score1[(x[0], x[1])]
	for y in missing:
		if score1[(y[0], y[1])] > score_un:
			n11 += 1
		elif score1[(y[0], y[1])] == score_un:
			n12 += 1
	score_un = score2[(x[0], x[1])]
	for y in missing:
		if score2[(y[0], y[1])] > score_un:
			n21 += 1
		elif score2[(y[0], y[1])] == score_un:
			n22 += 1
	score_un = score3[(x[0], x[1])]
	for y in missing:
		if score3[(y[0], y[1])] > score_un:
			n31 += 1
		elif score3[(y[0], y[1])] == score_un:
			n32 += 1

accuracy1 = ((n11 + (0.5 * n12)) / total1)

total2 = len(missing) * len(unconnected)

accuracy2 = ((n21 + (0.5 * n22)) / total2)

total3 = len(missing) * len(unconnected)

accuracy3 = ((n31 + (0.5 * n32)) / total3)

print("Accuracy :: "+str((accuracy1+accuracy2+accuracy3)/3))

end_time = time.time()

print("Efficiency of total Model:: " + str(end_time - start_time) + " seconds")
