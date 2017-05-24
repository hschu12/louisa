#
# NETWORK GENERATOR
# GENERATES GRID, SMALL WORLD, R-MAT, COMPLETE AND RANDOM NETWORK
# 

import random
import numpy as np
import sys
import networkx as nx


def main(version):

	#
	# VARIABLES
	#
	
	ps = [0.2,0.5]
	max_caps = [1,20]

	if version == 'complete':
		no_examples = 100
		ns = [50,100,500,1000]
		neighbours = [6,10,24]
		multiple = [5,10,25]
	if version == 'small':
		no_examples = 1
		ns = [150]
		neighbours = [10]
		multiple = [2]
	

	# SMALL
	# RESTRICTION : neighbour must be even (s.t. neighbour/2 = int)   &   neighbour < n
	# 			    0 < p < 1	  
	
	# RANDOM
	# RESTRICTION : m <= (n^2 - 3n)   =>   m_multiplicator <= (n - 3)
	# (because : n^2 all possible edges - n edges from a node to itself - n edges out of t - n edges into s)
	
	
	'''
	# SMALL WORLD NETWORKS
	# 
'''
	for i in range(1,no_examples+1):
		for n in ns:
			for neighbour in neighbours:
				if neighbour < n:
					for p in ps:

						print('Small, n = ',n,', neighbours = ',neighbour,', p = ',p)
						adjM = smallWorldNetwork(n,neighbour,p)

					 	# Relabeling nodes  
						G = nx.from_numpy_matrix(adjM,create_using=nx.DiGraph())
						mapping = {0:'s',1:'t'}
						G = nx.relabel_nodes(G,mapping, copy=False)

						# Changing name of attribute from weight to capacity
						# and adding tabu attribute
						for (u,v) in G.edges():
							G[u][v]['capacity'] = G[u][v]['weight']
							G[u][v]['tabu'] = 0	
							del G[u][v]['weight']

				  		# Number of edges
						m = G.number_of_edges()

						# Finding edge connectivity
						edge_connectivity = nx.edge_connectivity(G,'s','t')
						
						p=int(10*p)

						# Save adjacency matrix in file
						nx.write_gexf(G,'Small.'+str(n)+'.'+str(neighbour)+'.'+str(p)+'.'+str(i)+'.gexf')
	
				
	# R-MAT NETWORKS
	# (Network similar to real networks)
	for i in range(1,no_examples+1):
		for n in ns:
			for sum_multiplicator in multiple:
				
				sum = sum_multiplicator*n

				print('R-MAT, n = ',n,', sum-multiplicator = ',sum_multiplicator)
				adjM = rmatNetwork(n,sum)
			      
			  	# Relabeling nodes  
				G = nx.from_numpy_matrix(adjM,create_using=nx.DiGraph())
				mapping = {0:'s',1:'t'}
				G = nx.relabel_nodes(G,mapping, copy=False)

				# Changing name of attribute from weight to capacity
				# and adding tabu attribute
				for (u,v) in G.edges():
					G[u][v]['capacity'] = G[u][v]['weight']
					G[u][v]['tabu'] = 0	
					del G[u][v]['weight']

		 		# Number of edges
				m = G.number_of_edges()

				# Finding edge connectivity
				edge_connectivity = nx.edge_connectivity(G,'s','t')
					
				# Save adjacency matrix in file
				nx.write_gexf(G,'R-MAT.'+str(n)+'.'+str(sum_multiplicator)+'.'+str(i)+'.gexf')

	 
	# COMPLETE NETWORKS
	# (Network where each node is connected to all other nodes)
	for i in range(1,no_examples+1):
		for n in ns:
			for cap in max_caps:

				print('Complete, n = ',n,', max-cap = ',cap)
				adjM = completeNetwork(n,cap)

				# Relabeling nodes  
				G = nx.from_numpy_matrix(adjM,create_using=nx.DiGraph())
				mapping = {0:'s',1:'t'}
				G = nx.relabel_nodes(G,mapping, copy=False)

				# Changing name of attribute from weight to capacity
				# and adding tabu attribute
				for (u,v) in G.edges():
					G[u][v]['capacity'] = G[u][v]['weight']
					G[u][v]['tabu'] = 0	
					del G[u][v]['weight']

				# Number of edges
				m = G.number_of_edges()

				# Finding edge connectivity
				edge_connectivity = nx.edge_connectivity(G,'s','t')
					
				# Save adjacency matrix in file
				nx.write_gexf(G,'Complete.'+str(n)+'.'+str(cap)+'.'+str(i)+'.gexf')
	
	    
	# RANDOM NETWORKS
	# Uniform distribution
	for i in range(1,no_examples+1):
		for n in ns:
			for m_multiplicator in multiple: 
				if m_multiplicator <= (n - 3):
	
					print('Random Uni, n = ',n,', m-multiplicator = ',m_multiplicator)

				  	# Number of edges
					m = m_multiplicator*n

					adjM = randNetwork(n,m,'uni')

				   	# Relabeling nodes  
					G = nx.from_numpy_matrix(adjM,create_using=nx.DiGraph())
					mapping = {0:'s',1:'t'}
					G = nx.relabel_nodes(G,mapping, copy=False)

					# Changing name of attribute from weight to capacity
					# and adding tabu attribute
					for (u,v) in G.edges():
						G[u][v]['capacity'] = G[u][v]['weight']
						G[u][v]['tabu'] = 0	
						del G[u][v]['weight']

					# Number of edges
					m = G.number_of_edges()

					# Finding edge connectivity
					edge_connectivity = nx.edge_connectivity(G,'s','t')
						
					# Save adjacency matrix in file
					nx.write_gexf(G,'Rand.Uni.'+str(n)+'.'+str(m_multiplicator)+'.'+str(i)+'.gexf')
	'''				
	
	# RANDOM NETWORKS
	# Exponential distribution
	for i in range(1,no_examples+1):
		for n in ns:
			for m_multiplicator in multiple: 
				if m_multiplicator <= (n - 3):

				  	# Number of nodes
					m = m_multiplicator*n

					adjM = randNetwork(n,m,'exp')

				   	# Relabeling nodes  
					G = nx.from_numpy_matrix(adjM,create_using=nx.DiGraph())
					mapping = {0:'s',1:'t'}
					G = nx.relabel_nodes(G,mapping, copy=False)

					# Changing name of attribute from weight to capacity
					# and adding tabu attribute
					for (u,v) in G.edges():
						G[u][v]['capacity'] = G[u][v]['weight']
						G[u][v]['tabu'] = 0	
						del G[u][v]['weight']

					# Number of edges
					m = G.number_of_edges()

					# Finding edge connectivity
					edge_connectivity = nx.edge_connectivity(G,'s','t')
						
					# Save adjacency matrix in file
					nx.write_gexf(G,'Rand.Exp.'+str(n)+'.'+str(m_multiplicator)+'.'+str(i)+'.gexf')


	# RANDOM NETWORKS
	# Gauss distribution with variance 0.1
	for i in range(1,no_examples+1):
		for n in ns:
			for m_multiplicator in multiple: 
				if m_multiplicator <= (n - 3):

				  	# Number of nodes
					m = m_multiplicator*n

					adjM = randNetwork(n,m,'gauss01')

				   	# Relabeling nodes  
					G = nx.from_numpy_matrix(adjM,create_using=nx.DiGraph())
					mapping = {0:'s',1:'t'}
					G = nx.relabel_nodes(G,mapping, copy=False)

					# Changing name of attribute from weight to capacity
					# and adding tabu attribute
					for (u,v) in G.edges():
						G[u][v]['capacity'] = G[u][v]['weight']
						G[u][v]['tabu'] = 0	
						del G[u][v]['weight']

				 	# Number of edges
					m = G.number_of_edges()

					# Finding edge connectivity
					edge_connectivity = nx.edge_connectivity(G,'s','t')
						
					# Save adjacency matrix in file
					nx.write_gexf(G,'Rand.Gauss01.'+str(n)+'.'+str(m_multiplicator)+'.'+str(i)+'.gexf')

'''
	# RANDOM NETWORKS
	# Gauss distribution with variance 0.25 
	for i in range(1,no_examples+1):
		for n in ns:
			for m_multiplicator in multiple: 
				if m_multiplicator <= (n - 3):

					# Number of nodes
					m = m_multiplicator*n

					adjM = randNetwork(n,m,'gauss025')

				   	# Relabeling nodes  
					G = nx.from_numpy_matrix(adjM,create_using=nx.DiGraph())
					mapping = {0:'s',1:'t'}
					G = nx.relabel_nodes(G,mapping, copy=False)

					# Changing name of attribute from weight to capacity
					# and adding tabu attribute
					for (u,v) in G.edges():
						G[u][v]['capacity'] = G[u][v]['weight']
						G[u][v]['tabu'] = 0	
						del G[u][v]['weight']

					# Number of edges
					m = G.number_of_edges()

					# Finding edge connectivity
					edge_connectivity = nx.edge_connectivity(G,'s','t')
						
					# Save adjacency matrix in file
					nx.write_gexf(G,'Rand.Gauss025.'+str(n)+'.'+str(m_multiplicator)+'.'+str(i)+'.gexf')

	

	
















#
# R-MAT NETWORK GENERATOR (INTEGER CAPACITIES)
#

def rmatNetwork(n,sum,a=0.5,b=0.2,c=0.2,d=0.1):

  # n is the number of nodes
  # sum is the total sum of capacities in the network
  # a, b, c, d is the probabilities of distributing in the 
  # a: upper left, b: upper right, c: lower left and d: lower right windows

  adjMatrix = np.zeros(shape=(n,n))
  k = sum
  while k>0:
    imax = n
    imin = 0
    jmax = n
    jmin = 0
    while imax - imin > 1 and jmax - jmin > 1:
      r = random.random()
      δj = int(round((jmax + jmin) / 2))
      δi = int(round((imax + imin) / 2))
      if r < a:
        imax = δi
        jmax = δj
      else:
        if r < a+b:
          imin = δi
          jmax = δj
        else:
          if r < a+b+c:
            imax = δi
            jmin = δj
          else:
            imin = δi
            jmin = δj
    if imax != jmax:
      adjMatrix[(imax-1), (jmax-1)] += 1
      k -= 1
  
  return adjMatrix


#
# COMPLETE NETWORK GENERATOR
#

def completeNetwork(n,max_cap):

  # n is number of nodes
  # max_cap is the maximum capacity on any edge
  # capacities are uniformly distributed on the range 0 - max_cap

  # Creating adjacency matrix with random (from uniform distr) capacities
  if max_cap == 1:
  	adjMatrix = np.random.rand(n,n)
  else:	
  	adjMatrix = np.random.randint(1,max_cap,(n,n))
  
  # Erasing all edges from one node to it self
  for i in range(0,n):
    adjMatrix[i,i] = 0
  
  return adjMatrix

#
# RANDOM NETWORK GENERATOR
# 

def randNetwork(n,m,distr):

  adjMatrix = np.zeros(shape=(n,n))
  edges = 0 

  while edges < m:
    # Finding a tail for an edge
    # Probability 2/n for s, zero for t and 1/n for all other nodes
    tail = random.randint(0,(n-1))
    if tail == 1:
      tail = 0
    #print('tail : ',tail) 

    # Finding a head for an edge
    # Probability 2/n for t, zero for s and 1/n for all other nodes
    head = random.randint(0,(n-1))
    if head == 0:
      head = 1
    #print('head : ',head)
      
    # Finding the capacity for the edge
    
    # Uniform distribution
    if distr == 'uni':
      #print('distr : ',distr)	
      cap = random.uniform(0,1)
    # Gauss distribution with variation 0.1
    if distr == 'gauss01':
      cap = random.gauss(0.5,0.1)
    # Gauss distribution with variation 0.25
    if distr == 'gauss025':
      cap = random.gauss(0.5,0.25)
    # Exponential distribution
    if distr == 'exp':
      cap = random.expovariate(2)
    
    # Adding the edge to the ajdacency matrix if the edge does not exist already
    if adjMatrix[tail,head] == 0:
      adjMatrix[tail,head] = cap
      # Update edge count (not if edge is from a node to itself)
      if head != tail:
        edges = edges + 1
        
  # Erasing all edges from one node to itself
  for i in range(0,n):
    adjMatrix[i,i] = 0
 
  return adjMatrix
 
#
# SMALL WORLD NETWORK GENERATOR
#

def smallWorldNetwork(n,neighbours,p):

	k = neighbours

	node_list = list()
	for i in range(0,n):
		node_list.append(i)
	for i in range(0,int(k/2)):
		node_list.append(i)
    
	adjM = np.zeros(shape=(n,n))

	# First create the regular network
	for i in range(0, n):
		for j in range(i , int(i+k/2+1)):
			l = node_list[j]
			adjM[i][l] = 1
			adjM[l][i] = 1

	# Erasing all edges from one node to itself
	for i in range(0,n):
		adjM[i,i] = 0
 
	#
	# Adding randomness
	#

	# For each neighbour rank n_rank: 1 up to k/2
	for n_rank in range(1,int(k/2+1)):
		# For each node i
		for i in range(0,n):
			# With probability p
			r = random.random()
			if r < p:
				# Remove edge between the node i and its neighbour of rank n_rank
				j = node_list[i+n_rank]
				adjM[i][j] = 0
				adjM[j][i] = 0
				# Find a new random edge
				new_edge = False
				e_list = list()
				while new_edge == False:
					# If there are no new possibilities keep the old edge
					if len(e_list) == n:
						adjM[i][j] = 0
						adjM[j][i] = 0
						new_edge = True
					# Otherwise make a new edge from i to a random node
					# Not to itself and not where there already are an edge
					else:
						e = random.randint(0,n-1)
						# (Keep track of if all edges have been tried)
						if e not in e_list:
							e_list.append(e)
						if e != i and e != j and adjM[i][e] == 0:
							adjM[i][e] = 1
							adjM[e][i] = 1
							new_edge = True
              
	return adjM



#
# EXTENDED GRID NETWORK
#

def extendedGridNetwork(x,y):

	n = x*y
	G = nx.grid_2d_graph(x,y)

	# Renaming nodes
	labels = dict(((i,j),(i+1)+j*x) for i,j in G.nodes())
	G = nx.relabel_nodes(G,labels, copy=False)

	# Add edges from s and to t
	for u in G.nodes():
		if u < (x+1):
			G.add_edge(0,u)
		if u > (x*(y-1)):
			G.add_edge(u,n+1)
	    
	# Create adjacency matrix
	adjM = np.zeros(shape=(n+2,n+2))
	for u,v in G.edges():
		adjM[u][v] = 1
		adjM[v][u] = 1

	return adjM
  



main(sys.argv[1]) 











