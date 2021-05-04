import random, math, time
import igraph
import functools
from igraph import *

start_time = time.time()

graph = igraph.read("jazz.net", format = "pajek")
# graph = Graph.Read_GML("karate.gml")

Graph = graph.get_adjacency()		# future testing set

N = len(Graph[0]) # number of nodes in graph

futureGraph = []
currentGraph = []

for i in range(0, N):
	futureGraph.append([])
	currentGraph.append([])

edge = 0 	# number of edges present in futureGraph
edges = []	# list of edges present 

unconnected = [] # edges which are not in either currentGraph or FutureGraph
missing = [] # edges which are constructed between training and testing data

for i in range(0, N):
	for j in range(i + 1, N):
		if Graph[i][j]:
			edges.append((i, j))
			futureGraph[i].append(j)
			futureGraph[j].append(i)
			currentGraph[i].append(j)
			currentGraph[j].append(i)
			edge += 1
		else:
			unconnected.append((i, j))

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
	for y in range(x + 1, N):
		inter = 0
		union = 0
		score[(x,y)]=0
		for i in range(0, N):
			if (i in currentGraph[x]) and (i in currentGraph[y]):
				inter += 1
			if (i in currentGraph[x]) or (i in currentGraph[y]):
				union += 1
		if union > 0:
			score[(x, y)] = inter / union

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

AUC = ((n1 + (0.5 * n2)) / total)

TotalPrecision = 0
TotalRecall = 0

X = -1
def scorewise(p, q):
	return score[(min(X, p), max(X, p))] > score[(min(X, q), max(X, q))]

for x in range(0, N):
	top_links = []
	for y in range(0, N):
		if y != x and ((y in currentGraph[x]) == 0):
			top_links.append(y)

	X = x
	sorted_top_links = sorted(top_links, key=functools.cmp_to_key(scorewise))
	
	count = 0
	nums = len(sorted_top_links) / 2
	cur = 0
	for y in sorted_top_links:
		if count > nums:
			break
		count += 1
		if ((min(x, y), max(x, y)) in missing):
			cur += 1

	TotalPrecision += (cur / count)
	TotalRecall += (cur / len(missing))

TotalPrecision = TotalPrecision / N
TotalRecall = TotalRecall / N

end_time = time.time()

# Result print
print("Number of Nodes in Graph :: " + str(N))
print("Number of Edges in Graph :: " + str(edge))
print("AUC of the Model :: " + str(AUC))
print("Precision of the Model :: " + str(TotalPrecision))
print("Recall of the Model :: " + str(TotalRecall))
print("Efficiency of the Model :: " + str(end_time - start_time) + " seconds")
