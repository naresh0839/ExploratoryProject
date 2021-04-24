from igraph import *
import igraph
import random
import math
import time

start_time = time.time()

graph = igraph.read("jazz.net", format = "pajek")

futureGraph = graph.get_adjacency()		# future testing set
currentGraph = graph.get_adjacency()	# training set

N = len(futureGraph[0]) # number of nodes in graph

print(N)
edge = 0 	# number of edges present in futureGraph
edges = []	# list of edges present 

unconnected = [] # edges which are not in either currentGraph or FutureGraph
missing = [] # edges which are constructed between training and testing data

for i in range(0, N):
	for j in range(i + 1, N):
		if (futureGraph[i][j]):
			edges.append((i, j))
			edge = edge + 1
		else:
			unconnected.append((i, j))

delete = int(edge / 10)

for i in range(0, delete):
	idx = random.randrange(0, len(edges))
	it = edges[idx]
	edges.remove(it)
	missing.append(it)
	currentGraph[it[0]][it[1]] = 0
	currentGraph[it[1]][it[0]] = 0

deg = [0] * N

for i in range(0, N):
	for j in range(0, N):
		deg[i] += currentGraph[i][j]

score = []

for x in range(0, N):
	temp = []
	for y in range(0, N):
		CN = []
		for i in range(0, N):
			if (currentGraph[x][i] == 1 and currentGraph[y][i] == 1):
				CN.append(i)
		Score = 0
		for z in CN:
			if(deg[z] > 1):
				Score += 1 / math.log(deg[z])    # deg[z] = 1 isn't possible because it is intersection of two Nodes
		temp.append(Score)
	score.append(temp)

total = len(missing) * len(unconnected)
# total is the number of times that we randomly pick a pair of links from missing links set and unconnected links set
n1 = 0 
# n1 is the number of times that the missing link got a higher score than unconnected link
n2 = 0
# n2 is the number of times when they are equal

for x in unconnected:
	score_un = score[x[0]][x[1]]
	for y in missing:
		if score[y[0]][y[1]] > score_un:
			n1 += 1
		elif score[y[0]][y[1]] == score_un:
			n2 += 1

accuracy = ((n1 + (0.5 * n2)) / total)
print("Accuracy of the Model :: " + str(accuracy))
acc = (accuracy - 0.5) / 0.5 * 100
# print(str(acc) + "%")

end_time = time.time()

print("Efficiency of the Model :: " + str(end_time - start_time) + " seconds")
