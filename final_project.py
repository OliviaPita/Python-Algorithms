# Final Project
# by Olivia Pita
# for CSM IV: Algorithms
# 4/21/2025



# In a graph, what is the shortest path from a node start to a node end?
def algorithm_1(graph, start, end):     #start and end are strings, names of nodes
    visited = [False] * len(graph)      #which nodes have been visited
    previous = [None] * len(graph)      #node on the path with the shortest connection to each node
    distances = [float("inf")] * len(graph)     #distance of each node from start

    idx_map = {key: i for i, key in enumerate(graph)}   #allows for finding index of a key
        #this is needed for visited[] and previous[]

    distances[idx_map.get(start)] = 0
    queue = [(start,0)]

    while queue and queue[0][1] != end:     #keep checking the edges of every node until the end becomes the node to check
        node,dis_from_start = queue.pop(0)
        
        visited[idx_map.get(node)] = True
        connections = graph[node] #this is a list of tuples (connected_node, weight)

        #for each connection, if it provides a shorter path to a target node than currently available,
        #record the shorter path
        for conn in connections:
            new_distance = dis_from_start + conn[1]
            node2_index = idx_map.get(conn[0])
            if new_distance < distances[node2_index]:
                distances[node2_index] = new_distance   #set total distance to next node
                previous[node2_index] = node            #set current as previous of next node
                queue.append((conn[0], new_distance))   #next node

    #create string describing path
    #work backworks to create a stack of nodes visited from end to start
    stack = [end]
    while stack[-1] != start:
        stack.append(previous[idx_map.get(stack[-1])])
    #reverse the stack so it's in order from start to end, then convert it to a pretty string
    stack.reverse()
    path_string = " -> ".join(stack)

    return distances[idx_map.get(end)], path_string



def algorithm_2(graph, start):
    visited = [False] * len(graph)  #which nodes have been visited
    stack = []  #items in stack will be "edge" tuples of form (node1, node2, cost)
    MST = []
    node = start
    idx_map = {key: i for i, key in enumerate(graph)}  #allows for finding index of a key
        #this is needed for visited[] and previous[]

    while not all(visited) and node != None:
        visited[idx_map.get(node)] = True

        #for each unvisited connected node, add the edge to that node to the stack
        connections = graph[node] #this is a list of tuples (connected_node, weight)
        for conn in connections:
            if not visited[idx_map.get(conn[0])]:
                stack.append([node, conn[0], conn[1]])

        #find shortest edge in stack, working backwards to avoid index errors
        shortest_edge = (None, None, float("inf"))
        i = len(stack) - 1
        while i >= 0:
            node1 = stack[i][0] #first item in tuple
            node2 = stack[i][1]
            cost = stack[i][2]
            
            if visited[idx_map.get(node1)] and visited[idx_map.get(node2)]:
                stack.pop(i)    #if node1 and node2 are already connected in the MST, delete their edge from stack
            else:
                if cost < shortest_edge[2]:
                    shortest_edge = (node1, node2, cost)
            i -= 1

        #once the shortest is is found, if it isn't a None edge...
        if shortest_edge[0] and shortest_edge[1]:
            stack.remove(list(shortest_edge))   #...remove from stack...
            MST.append(shortest_edge)   #...and add to MST
        node = shortest_edge[1]

    return MST



def algorithm_3(graph, start, to_remove, to_add):

    for edge in to_remove:
        node1 = edge[0]
        node2 = edge[-1]

        #remove edge connection for node1's list
        conn_index = 0
        for connection in graph[node1]:
            if connection[0] == node2:
                del graph[node1][conn_index]
            conn_index += 1

        #remove edge connection for node2's list
        conn_index = 0
        for connection in graph[node2]:
            if connection[0] == node1:
                del graph[node2][conn_index]
            conn_index += 1

    for edge in to_add:
        node1 = edge[0]
        node2 = edge[1]
        cost = edge[2]

        #check if the edge already exists
        exists = False
        for connection in graph[node1]:
            if connection[0] == node2:
                exists = True
                break
        if not exists:
            graph[node1].append((node2, cost))
            graph[node2].append((node1, cost))

    return algorithm_2(graph, start)





##### MAIN

example_graph = {
	"A": [("B", 1), ("C", 4)],
	"B": [("A", 1), ("C", 2), ("D", 3)],
	"C": [("A", 4), ("B", 2), ("D", 6)],
	"D": [("B", 3), ("C", 6)],
}

example_graph_2 = {
	"Z": [("X", 2)],
	"Y": [("W", 1), ("U", 2)],
	"X": [("Z", 2), ("U", 4)],
	"W": [("Y", 1), ("U", 1)],
	"U": [("Y", 2), ("X", 4), ("W", 1)],
}


### Algorithm 1

#Test 1: Does the algorithm recognize that the most direct path is not always the most efficient?
# start at A and end at C
print(algorithm_1(example_graph, "A", "C"))
# Cost: 3
# Shortest Path: A -> B -> C

#Test 2: Does the algorithm recognize that the most direct path *can* be the most efficient?
# start at A and end at B
print(algorithm_1(example_graph, "A", "B"))
# Cost: 1
# Shortest Path: A -> B

#Test 3: Does the algorithm work when a decision between "shortest" and "directest" is not from the start node?
# start at D and end at C
print(algorithm_1(example_graph, "D", "C"))
# Cost: 5
# Shortest Path: D -> B -> C


### Algorithm 2

#Test 1: Generic test.
# start at A (the hub location)
print(algorithm_2(example_graph, "A"))
# MST: [(A, B, 1), (B, C, 2), (B, D, 3)]

#Test 2: Same graph but starting from a different node.
# start at D (the hub location)
print(algorithm_2(example_graph, "D"))
# MST: [(D, B, 3), (B, A, 1), (B, C, 2)]

#Test 3: Different graph, where the start node ends up in the middle of the path.
# start at U (the hub location)
print(algorithm_2(example_graph_2, "U"))
# MST: [(U, W, 1), (W, Y, 1), (U, X, 4), (X, Z, 2)]


### Algorithm 3

#Test 1: Remove one route, add one route.
# starts at A (the hub location), removed A-B edge, and adds A-D edge with a weight of 3
print(algorithm_3(example_graph, "A", ["A-B"], [("A", "D", 3)]))
# MST: [(A, D, 3), (D, B, 3), (B, C, 2)]

#Reset example_graph to original state
algorithm_3(example_graph, "A", ["A-D"], [("A", "B", 1)])

#Test 2: Remove two routes.
# starts at A (the hub location), removed A-B edge and B-D edge
print(algorithm_3(example_graph, "A", ["A-B", "B-D"], []))  ###GLITCH because previous statement modified the graph, not a copy
# MST: [(A, C, 4), (C, B, 2), (C, D, 6)]

#Test 3: Different graph, add two routes.
# starts at U (the hub location), added Z-Y edge with weight 3 and 
print(algorithm_3(example_graph_2, "U", [], [("Z", "Y", 3), ("W", "X", 1)] ))
# MST: [(U, W, 1), (W, X, 1), (W, Y, 1), (X, Z, 2)]

