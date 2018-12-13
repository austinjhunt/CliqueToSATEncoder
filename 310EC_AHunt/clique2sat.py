""" Austin Hunt; December 11, 2018 
I certify that this is entirely my own work; I consulted many resources in developing my plan for
the encoding, most of which were published academic papers, the rest of which consisted of 
an IBM presentation and some books from the Addlestone Library."""
import itertools
import time # use for timing normal exhaustive search algorithm
import numpy as np # use for matrix displays

 # create a directory for each k 
import os   

# input a graph adjacency matrix

# output a string in DIMACS format representing an instance
# of a SAT problem that has a one-to-one map to a clique problem of
# size k for this input graph

class Clique2SATEncoder:
	def __init__(self, adj,k):
		self.adj = adj # G = {V, E}
		self.k = k # want to find clique of size k
		self.clique = [] #initialize clique to empty set on instantiation

	def generateDIMACS(self):

		# we need to define a list of variables x_{iv} :
			# for every vertex in V (G = {V, E}
			# for every i between 1 and k
			# these variables will each need to be integers -->
				# integers represent boolean literals in DIMACS format
		numVertices = len(self.adj)

		literal = 1
		literal_dict = {} # to mimic our x_{iv} we can let x be an integer key, and let i,v be a tuple stored as that key's value
		DIMACS = ""
		clause_list = []



		# CONSTRAINT 1)
		# We want to say, for every i, there is an ith vertex in the clique
		# equivalent to: v0 is 1st or v1 is 1st or... vn is 1st
		# AND
		# v0 is 2nd or v1 is 2nd or v2 is 2nd.... etc
		# -> encode
		#  (x_1,0) or (x_1,1) or (x_1,2).... (x_1, n) where n = last vertex
		# AND
		# (x_2,0) or (x_2,1) or (x_2,2).... (x_2, n) where n = last vertex
		# AND
		# ...
		# (x_k,0) or (x_k,1) or (x_k,2).... (x_k, n) where n = last vertex

		# can create literals and encode constraint 1 using the same loop
		# since they require the same algorithm structure
		#print("K = ",self.k)
		for i in range(1, self.k + 1): # for 1..i..k ; + 1 since range end is exclusive
			#print("Encoding for i = ", i)
			# new clause for each i to encode constraint 1
			clause = ''
			for v in range(numVertices): # for each vertex in V
				literal_dict[literal] = [i,v] # store <int>_{iv}

				clause += str(literal) + " "

				# next literal
				literal += 1  # go to next integer

			# end of clause, add a 0
			clause += "0"
			#append clause to list
			clause_list.append(clause)


		# now have our dictionary of x_ivs stored as x: [i,v] where x is an integer 1....n
		#  (n will be the number of literals in our CNF formula

		# CONSTRAINT 2) for every non edge (v,w) (i.e. 0 in adjacency matrix), v and w cannot BOTH be in C (clique)
		# look thru adjacency matrix, if you reach a 0, this is a non-edge,
		# so add a clause representing not x_iv or not x_iw
		# both x_iv and x_iw are represented by literals
		#print('constraint 2')
		for literal1 in literal_dict:
			v = literal_dict[literal1][1]
			i = literal_dict[literal1][0]
			for literal2 in literal_dict:
				#print("Literal1,literal2:",literal1,literal2)
				w = literal_dict[literal2][1]
				j = literal_dict[literal2][0]

				# Encode Constraint 2
				# now, are the v and w NOT adjacent in the original graph?
				if self.adj[v][w] == 0 and v != w and literal1 != literal2: # add last part to keep a contradiction from occurring
					# if not adjacent add clause not x_iv or not x_iw
					clause = "-" + str(literal1) + " -" + str(literal2) + " 0"
					if clause not in clause_list:
						clause_list.append(clause)

				# Encode Constraint 3
				#  want to add a clause saying if the two vertices are the same, but their i and j are different,
				# then not literal1 or not literal 2
				if v == w and i != j and literal1 != literal2: # add last part to keep a contradiction from occurring: # same vertex cant be both ith and jth in clique
					clause = "-" + str(literal1) + " -" + str(literal2) + " 0"
					if clause not in clause_list:
						clause_list.append(clause)

				# on that same note, if i and j are equal and v and w are not equal, do the same thing
				# because two vertices cannot be both the i=jth vertex in the clique
				if v != w and i == j and literal1 != literal2: # add last part to keep a contradiction from occurring: # same vertex cant be both ith and jth in clique
					clause = "-" + str(literal1) + " -" + str(literal2) + " 0"
					if clause not in clause_list:
						clause_list.append(clause)

		# Combine this into the above loop structure to avoid unnecessarily doubling the time (same nested loop, different basic ops, no need to repeat)
		# CONSTRAINT 3) for every i, j (in x_iv, x_jv) ith vertex is not the same as jth vertex: not x_iv  or not x_jv
		# want to check the "i" and "j" of literal1: i,v and literal2: j,v
		# other way of saying this: a vertex cannot be both the ith and the jth vertex in the clique
		#for literal1 in literal_dict:
		#    v = literal_dict[literal1][1]
		#    i = literal_dict[literal1][0] # overall bool: v is the ith vertex of the clique
		#    for literal2 in literal_dict:
				#print("Literal1,literal2:",literal1,literal2)
		#        w = literal_dict[literal2][1]
		#        j = literal_dict[literal2][0] # overall bool: w is the jth vertex of the clique

				#  want to add a clause saying if the two vertices are the same, but their i and j are different,
				# then not literal1 or not literal 2
		#        if v == w and i != j and literal1 != literal2: # add last part to keep a contradiction from occurring: # same vertex cant be both ith and jth in clique
		 #           clause = "-" + str(literal1) + " -" + str(literal2) + " 0"
		#            if clause not in clause_list:
		#                clause_list.append(clause)

				# on that same note, if i and j are equal and v and w are not equal, do the same thing
		 #       # because two vertices cannot be both the i=jth vertex in the clique
		 #       if v != w and i == j and literal1 != literal2: # add last part to keep a contradiction from occurring: # same vertex cant be both ith and jth in clique
		#            clause = "-" + str(literal1) + " -" + str(literal2) + " 0"
		 #           if clause not in clause_list:
		 #               clause_list.append(clause)

		#print(literal_dict[1],literal_dict[3],literal_dict[6],literal_dict[9],literal_dict[11])
		# for DIMACS first line
		numLiterals = len(literal_dict)
		numClauses = len(clause_list)

		DIMACS = ""
		firstLine = "p cnf " + str(numLiterals) + " " + str(numClauses)

		DIMACS += firstLine + '\n'

		# add any comments you want
		comments = ['c each literal represents x_iv indicating vertex v is ith vertex of clique']
		for c in comments:
			DIMACS += c


		# now add the clauses
		for c in clause_list:
			DIMACS += '\n' + c

		return DIMACS


# class for solving clique problem without SAT encoding
# using for comparisons
class CliqueSolver:
	def __init__(self,adj):
		self.adj = adj
		self.vertexList = [i for i in range(len(self.adj))]

	# return clique of size k if it exists, false otherwise
	def findClique(self,k):
		start_time = time.time()

		n = len(self.adj)
		# need to look at all n choose k combinations of vertices, and see if it's a clique
		numCombinations = self.choose(n,k)

		all_combinations_size_k = itertools.combinations(self.vertexList,k)

		# need to see if each pair in each combination is connected!
		# numPairs will be constant since all groups are same size k
		cliques = [] # store all the cliques in this list

		for possibleClique in all_combinations_size_k:
			#print("Possible clique:",possibleClique)
			all_pairs = itertools.combinations(possibleClique,2) # generate all_pairs
			is_clique = True
			for pair in all_pairs:
				v,w = pair[0],pair[1]
				if self.adj[v][w] == 0:
					is_clique = False
					break
			if is_clique:
				# made it through all pairs without breaking, so this is a clique
				cliques.append(possibleClique)

		if len(cliques) > 0:
			return cliques, str(round(time.time() - start_time, 4)) + "s"
		else:
			return False, str(round(time.time() - start_time,4)) + "s"


	# need to look at n choose k combinations of vertices
	def choose(self,n,k):
		return self.factorial(n) // (self.factorial(k)*self.factorial(n-k))

	def factorial(self,n):
		f = 1
		for i in range(1,n+1):
			f = f * i
		return f



# define a method that generates a random graph
# with v vertices and e edges (randomly connecting any two vertices v,w such that v isn't
# the same vertex as w
# For testing, we want to pass in graphs of various sizes and see how the required time
#  for the sat solver to solve the problem
# changes;
# idea: use a for loop, creating increasingly larger graphs and invoking the encoder on each graph
# output each unique dimacs string to a separate text file

# define method to generate random adjacency matrix of length v with e random edges (this is for undirected, so
# assume symmetrical across diagonal meaning i,j = 1 and j,i = 1 does not count as two edges
import random # use to randomly decide between add edge, don't add edge, for i, j pair
def generategraph(v,e):

	# need v rows and columns
	adj = []
	# initialize to all 0s
	for i in range(v):
		adj.append([])
		for j in range(v):
			adj[i].append(0)

	edges_added = 0 # var to keep track of num edges added

	# its possible entire matrix is generated without adding the full number of requested edges on first
	# iteration of for i in range(v), so put the double nested loop structure in a while loop dependent on the edges_added counter
	# on iteration i > 2, only use randint if current i, j value is 0; don't want to change a 1 to a 0
	iteration = 0

	choice_list =[0] * 25 + [1] # use for randomly selecting 0 or 1; explanation below
	while edges_added < e:
		for i in range(v):
			for j in range(v):
				# lets constrain our edge additions to upper half, meaning only add edge randomly if i < j
				if i < j and adj[i][j] == 0:
					# cant use just randint(0,1); tried this, but all edges concentrate
					# toward top of matrix; so decrease chance of 1 to make distribution more
					# uniform for larger matrices
					add_edge = random.choice(choice_list)
					if add_edge == 1:
						edges_added += 1
					adj[i][j] = add_edge
					# make this symmetric
					adj[j][i] = adj[i][j]
					# if you've reached requested number of edges, then stop
					if edges_added >= e:
						return adj
				# only do this on first iteration, waste to keep doing it
				if i == j and iteration == 0:
					adj[i][j] = 0
		iteration += 1


# define a method to interpret the valuation output by the sat solver if it does give a valuation
def interpretSATval(literalstring,literal_dict): 
    literal_list = literalstring.split()
    print(literal_list)

    # need the original literal_dict that was used 
    # key: value -> literal: [i,v] -> v is the ith vertex of the clique
    # initialize clique to empty list
    clique = []
    interpretation = ""
    for literal in literal_list: 
        # if literal not preceded by - in output, then v is in clique
        if "-" not in literal: 
            i_v = literal_dict[literal]
            clique.append(i_v)
            interpretation += "Vertex " + str(i_v[1]) + " IS the " + str(i_v[0]) + "th vertex of the clique.\n"
        else: 
            interpretation += "Vertex " + str(i_v[1]) + " is NOT the " + str(i_v[0]) + "th vertex of the clique.\n"

    return interpretation

   




import multiprocessing as mp

# using a 2cpu windows vm with Azure portal, take advantage of multiprocessing to build DIMACS strings
def genDIMACSinstance(k,v_e_list):
	print("\n\n\n")
	print(mp.current_process(),"VE LIST: ", v_e_list)
	for v_e_tuple in v_e_list: 
		v,e = v_e_tuple[0],v_e_tuple[1]
		print("V,E:",v,e)
		# only worry about this instance if the current k < = v
		if k <= v: 
			title = "Clique Instance: Does a clique of size k = " + \
			str(k) + "exist in G = (V,E) where |V| =" + str(v) + "and |E| = " + str(e) + "?"

			#generate graph
			graph = generategraph(v,e)
			# convert to string for writing
			#graphstring = '\n'.join('\t'.join('%0.3f' %col for col in row) for row in graph)
			# for each graph, write to its own file, then generate dimacs string 
			# and write that to the same file as well
			fileName = "graph_" + str(v) + "E_" + str(e) + "E.txt"
			f = open(fileName,"w")
			# write the title
			f.write(title + "\n")

			# go ahead and test the exhaustive search on thisi instance
			found,time =eexSearcher = CliqueSolver(adj=graph).findClique(k)

			# append the found,time output and matrix and dimacs
			f = open(fileName,"a")

			f.write("found: " + str(found) + "\n")
			f.write("time: " + time + "\n")

			f.write("Graph Adjacency Matrix:\n")
			f.write(str(graph))

			f.write("\n\n\n")

			f.write("DIMACS String:\n")
			# generate and append the dimacs string for current graph and k value
			dimacs = Clique2SATEncoder(adj=graph, k=k).generateDIMACS()
			f.write(dimacs)


def docurrentkstuff(k,owd,v_e_list_small,v_e_list_big):

	os.chdir(owd)
	# create a directory for each k 
	# define the name of the directory to be created
	path = "clique_of_k_" + str(k)
	try:  
		os.mkdir(path)
	except OSError:  
		print ("Creation of the directory %s failed" % path)

	print ("Successfully created the directory %s " % path)
	os.chdir(path)
	print("starting ve tuple")
	print(os.getcwd())

	# Setup a list of processes that we want to run
	# Want one process for smaller sizes
	# 2 processes for big size
	childprocesses = [mp.Process(target=genDIMACSinstance, args=(k,arglist)) for arglist in [v_e_list_small,v_e_list_big,v_e_list_big]]
	# Run the processes
	for p in childprocesses:
		p.start()
		print("Starting",p)

	# Exit the completed processes
	for p in childprocesses:
		print("Ending",p)
		p.join()




def main():
	# lets generate various instances of each of the following graphs:
	# 5 nodes, 4 edges (small)
	# 100 nodes, 200 edges (medium)
	# 1000 nodes, 5000 edges (super big)
	# define list to store these values
	v_e_list_small = [[5,4], [10,15], [20,30], [50,80],[100,200]]
	v_e_list_big = [[1000,2000]] # WAY TOO SLOW TO INCLUDE THOUSANDS OF NODES/EDGES
	print(os.getcwd())
	# create and change to tests directory 
	path = "tests2"
	try: 
		os.mkdir(path)
	except OSError:  
		print ("Creation of the directory %s failed" % path)

	print ("Successfully created the directory %s " % path)
	os.chdir(path)
	owd = os.getcwd()
	
	# use many different values of k (2 <= k <= 30)
	# use one process per k
	klist = [2,6,10,20]
	kprocesses = s = [mp.Process(target=docurrentkstuff, args=(k,owd,v_e_list_small,v_e_list_big)) for k in klist]
	for kp in kprocesses:
		kp.start()
	for kp in kprocesses:
		kp.join()
    

if __name__ == '__main__':  
	main()

