import igraph
from igraph import *
import random
import math
import time

start_time = time.time()

#graph = Graph.Read_GML("karate.gml")
graph = igraph.read("jazz.net", format = "pajek")
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

score = {}

for x in range(0, N):
	temp = []
	for y in range(x + 1, N):
		Score = 0
		for i in range(0, N):
			if (i in currentGraph[x]) and (i in currentGraph[y]):
				Score += 1
		if(len(currentGraph[x])>0 and len(currentGraph[y])>0):
			Score = Score / math.sqrt(len(currentGraph[x]) * len(currentGraph[y]))
		score[(x, y)] = Score

total = len(missing) * len(unconnected)
# total is the number of times that we randomly pick a pair of links from missing links set and unconnected links set
n1 = 0
# n1 is the number of times that the missing link got a higher score than unconnected link
n2 = 0
# n2 is the number of times when they are equal

for x in unconnected:
	score_un = score[(x[0], x[1])]
	for y in missing:
		if score[(y[0], y[1])] > score_un:
			n1 += 1
		elif score[(y[0], y[1])] == score_un:
			n2 += 1

accuracy = ((n1 + (0.5 * n2)) / total)
print("Accuracy of the Model :: " + str(accuracy))
acc = (accuracy - 0.5) / 0.5 * 100
# print(str(acc) + "%")

end_time = time.time()

print("Efficiency of the Model :: " + str(end_time - start_time) + " seconds")
