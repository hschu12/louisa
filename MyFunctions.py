#
# COLLECTION OF FUNCTIONS USED IN LOCAL SEARCH ALGORITHM
# FOR FINDING BEST INTERDICTION VALUE
#

############# OVERVIEW ##################

# REMOVERANDOM
# REMOVECUT
# REMOVECARDCUT
# FINDROUTE
# SENDFLOW
# DELTACOST 
# PROB_IMPR
# SIM_AN

import networkx as nx
import random
import copy
from math import exp 
import time
import sys

#
# REMOVERANDOM
# Removes k random edges from G
#

def RemoveRandom(F,k):
	G = copy.deepcopy(F)
	k_set = list()
	for u,v in random.sample(G.edges(),k):
		k_set.append((u,v,G[u][v]['capacity'],0))
		G.remove_edge(u,v)
	return G, k_set

#
# REMOVECUT
# Removes k edges from G taking edges from the cut-set first
#

def RemoveCut(F,k):
	G = copy.deepcopy(F)
	k_set = list()
	counter = 0

	# Find min cut
	cut_value, partition = nx.minimum_cut(G, 's', 't')
	reachable, non_reachable = partition
	
	# Finding min st-cut set
	cut_set = list()
	for u,v in G.edges_iter():
		if u in reachable and v in non_reachable: 
			cut_set.append((u,v,G[u][v]['capacity']))

	# Sort cut set by descending capacities		
	cut_set.sort(key = lambda cut_set: cut_set[2], reverse = True)
	#print('Cut set : ',cut_set)
	#print('\n')

	# Removing edges from G and adding them to k-set
	for u,v,c in cut_set:
		if counter < k:
			k_set.append((u,v,c,0))
			G.remove_edge(u,v)
		counter += 1
	# If there 	are less than k edges in the cut set remove the last eges randomly
	cs=len(cut_set)
	if cs < k:
		for u,v in random.sample(G.edges(),(k-cs)):
			k_set.append((u,v,G[u][v]['capacity'],0))
			G.remove_edge(u,v)

	return G, k_set, cut_set

#
# REMOVECARDCUT
# Removes k edges from G taking edges from the cut with lowest cardinality
# 

def RemoveCardCut(F,k):
	G = copy.deepcopy(F)
	k_set = list()
	counter = 0

	# Finding st-cut with smalles cardinality
	card_set = nx.minimum_edge_cut(G,'s','t')
	
	# Sorting the cut by descending capacities
	card_cut_set = list()
	for u,v in card_set:
		card_cut_set.append((u,v,G[u][v]['capacity']))
	card_cut_set.sort(key = lambda card_cut_set: card_cut_set[2], reverse = True)
	print('Card cut set : ',card_cut_set)
	print('\n')
	
	# Removing edges from G and adding them to k-set
	for u,v,c in card_cut_set:
		if counter < k:
			k_set.append((u,v,c,0))
			G.remove_edge(u,v)
		counter += 1
	# If there 	are less than k edges in the cut set remove the last eges randomly
	cs=len(card_cut_set)
	if cs < k:
		for u,v in random.sample(G.edges(),(k-cs)):
			k_set.append((u,v,G[u][v]['capacity'],0))
			G.remove_edge(u,v)

	return G, k_set


#
# FINDROUTE
# Function that searches for a route from u to v in R using BFS
#

def FindRoute(K,u,v):
	R = copy.deepcopy(K)
	route = False
	# Reset parents
	for x in R.nodes():
		R[x]['parent'] = 'no'
		#print('x : ',x,' , parent : ',R[x]['parent'])
	#print('u : ',u)
	#print('v : ',v)
	# If u = v
	if u == v:
		print('There is no uv-route since u = v')
	# If u != v	
	else:
		# Initial
		S = set()
		Q = list()
		S.add(u)
		Q.append(u)
		# Search
		while len(Q) != 0 and route == False:
			x = Q.pop(0)
			for y in R[x]:
				if y != 'parent' and R[x][y]['res_cap'] > 0:
					if y not in S:
						S.add(y)
						R[y]['parent'] = x
						Q.append(y)
						#print('x : ',x,' , y : ',y,' , ys parent : ',R[y]['parent'])
						if y == v:
							route = True
							print('break')
							break
	'''
		# Print the route if it exists
		if route == True:					
			y = v
			x = R[y]['parent']
			print('x = ', x, ', y = ', y, ', res_cap = ', R[x][y]['res_cap'])
			while y != u:
				y = x
				x = R[y]['parent']
				if y != u:
					print('x = ', x, ', y = ', y, ', res_cap = ', R[x][y]['res_cap'])
	
	print('R : ')
	for u,v in R.edges():
		print(u, v, R[u][v])
	'''
	return route, R

#
# SENDFLOW
# Function that sends max possible flow from u to v in R
# where delta is an initial max 
#

def SendFlow(K,u,v,init_max):
	R = copy.deepcopy(K)
	
	# Backtracking to find the smallest delta (amount that can be sent)
	delta = init_max
	y = v
	x = R[y]['parent']
	#print(x,' ', y, ', res_cap = ', R[x][y]['res_cap'])
	while y != u:
		if R[x][y]['res_cap'] < delta:				
			delta = R[x][y]['res_cap']
		y = x
		x = R[y]['parent']
		#if y != u:
			#print(x,' ', y, ', res_cap = ', R[x][y]['res_cap'])
	#print('delta = ', delta)
	# Backtracking to send flow
	y = v
	x = R[y]['parent']
	while y != u:
		R[x][y]['flow'] = R[x][y]['flow'] + delta
		R[x][y]['res_cap'] = R[x][y]['res_cap'] - delta
		if (y,x) not in R.edges():
			R.add_edge(y,x)
			R[y][x]['capacity'] = 0
			R[y][x]['flow'] =  - delta
			R[y][x]['res_cap'] =  delta
		else:
			R[y][x]['flow'] = R[y][x]['flow'] - delta
			R[y][x]['res_cap'] = R[y][x]['res_cap'] + delta
		y = x
		x = R[y]['parent']

	'''
	print('\n')
	print('R : ')
	for u,v in R.edges():
		print(u, v, R[u][v])
	'''
	return R, delta

#
# DELTA COST FUNCTION
# Calculate new max-flow
#

def DeltaCost(K,new_k_edge,new_graph_edge,max_flow):
	print('Delta cost calculation')
	print('\n')

	R = copy.deepcopy(K)
	u,v,c,t = new_k_edge
	new_k_edge_value = R[u][v]['flow']
	print('new k edge value : ',new_k_edge_value)


	if (u,v) in R.edges():
		print('uv :',u,v,R[u][v])
	if (v,u) in R.edges():
		print('vu :',v,u,R[v][u])
	
	#
	# Remove new_k_edge from R
	#
	R.remove_edge(u,v)
	print('Removed edge u,v : ',u,v,' from R')

	#print('uv :',u,v,R[u][v])
	if (v,u) in R.edges():
		print('vu :',v,u,R[v][u])

	if new_k_edge_value > 0:
		if(v,u) in R.edges():
			if R[v][u]['flow'] > 0:
				R[v][u]['flow'] = R[v][u]['flow'] - R[u][v]['flow']
				R[v][u]['res_cap'] = R[v][u]['capacity'] - R[v][u]['flow']
				R[v][u]['tabu'] = t	

	if new_k_edge_value < 0:
		if (v,u) in R.edges():
			if R[v][u]['flow'] > 0:
				R.add_edge(u,v)
				R[u][v]['capacity'] = 0
				R[u][v]['flow'] = -R[v][u]['flow']
				R[u][v]['res_cap'] = R[u][v]['capacity'] - R[u][v]['flow']
				R[u][v]['tabu'] = t	
	# If there was flow on uv
#	if new_k_edge_value > 0:
		# If vu is not an original edge
#		if R[v][u]['capacity'] == 0:
#			R.remove_edge(v,u)
		# If vu is an original edge
#		if R[v][u]['capacity'] > 0:
#			R[v][u]['res_cap'] = R[v][u]['res_cap'] - new_k_edge_value
	
	print('\n')	
	print('R :')
	for x,y in R.edges():
		print(x,y,R[x][y])
	print('\n')

	delta_start_time = time.time()
	


	'''

	#
	# ALTERNATIVE DELTA COST CALCULATION
	#

	#		
	# Add new_grah_edge to R
	#
	u,v,c,t = new_graph_edge
	R.add_edge(u,v)
	#R.add_edge(v,u)
	R[u][v]['capacity'] = c
	#R[v][u]['capacity'] = 0.0
	R[u][v]['flow'] = 0.0
	#R[v][u]['flow'] = 0.0
	R[u][v]['res_cap'] = R[u][v]['capacity'] - R[u][v]['flow']
	#R[v][u]['res_cap'] = R[v][u]['capacity'] - R[v][u]['flow']	
	R[u][v]['tabu'] = t
	
	#
	# Calculate new max-flow
	#

	new_max_flow, flow_dict = nx.maximum_flow(R, 's', 't')






	'''
	#
	# If there used to be sent flow via uv = new_k_edge
	#
	print('new k edge flow value : ', new_k_edge_value)
	alpha = 0
	if new_k_edge_value > 0:
		delta = 0
		uv_route = True

		# As long as it is possible to find new paths 
		# and all flow (that used to be sent on uv) has not been sent yet
		print('search for new routes \n')
		while uv_route == True and delta < new_k_edge_value:
			# Search for alternative route from u to v (uv = new_k_edge) in R
			u,v,c,t = new_k_edge
			uv_route, R = FindRoute(R,u,v)
			print('uv_route : ', uv_route)

			# If there exists a uv-route: 
			# Send flow (of value delta= max possible via that alt. route) 
			# through alternative route and update R
			if uv_route == True:
				R, flow_value = SendFlow(R,u,v,(new_k_edge_value-delta))
				delta = delta + flow_value
				print('delta sent : ', delta)
				#print('R : ')
				#for u,v in R.edges():
				#	print(u, v, R[u][v])

		# If there remains uv-flow (of value alpha) 
		# send this back from u to s and from t to v in R
		alpha = new_k_edge_value - delta
		print('no more rutes available, send back ', alpha, ' to s and t')

		print('\n')
		print('alpha : ', alpha)
		alpha_sent_s = 0
		alpha_sent_t = 0
		if alpha > 0:
			# From u to s
			if u == 's':
				alpha_sent_s = alpha
				print('u = s')
			while alpha_sent_s < alpha:
				print('Finding route from s to u')
				us_route, R = FindRoute(R,u,'s')
				print('us_route : ', us_route)
				print('\n')
				if us_route == True:
					R, flow_value = SendFlow(R,u,'s',(alpha-alpha_sent_s))
					alpha_sent_s = alpha_sent_s + flow_value
					print('alpha_sent to s : ', alpha_sent_s)
					print('\n')
				print('alpha: ', alpha, ', alpha_sent_s: ', alpha_sent_s)
				if us_route == False:
					sys.exit(1)
			# From t to v
			if v == 't':
				alpha_sent_t = alpha
				print('v = t')
			while alpha_sent_t < alpha:
				tv_route, R = FindRoute(R,'t',v)
				print('tv_route : ', tv_route)
				print('\n')
				if tv_route == True:
					R, flow_value = SendFlow(R,'t',v,(alpha-alpha_sent_t))
					alpha_sent_t = alpha_sent_t + flow_value
					print('alpha_sent from t : ', alpha_sent_t)
				print('alpha: ', alpha, ', alpha_sent_t: ', alpha_sent_t)
				if tv_route == False:
					sys.exit(1)
	print('\n')
	
	delta_time = time.time() - delta_start_time
	
	#		
	# Add new_grah_edge to R
	#
	u,v,c,t = new_graph_edge
	print('new G edge : ',u,v)
	#R.add_edge(u,v)
	if (u,v) in R.edges():
		R[u][v]['capacity'] = R[u][v]['capacity'] + c
		R[u][v]['res_cap'] = R[u][v]['capacity'] - R[u][v]['flow']
		R[u][v]['tabu'] = t
	else:	
		R[u][v]['capacity'] = c
		R[u][v]['flow'] = 0.0
		R[u][v]['res_cap'] = R[u][v]['capacity'] - R[u][v]['flow']
		R[u][v]['tabu'] = t
	
	#for x,y in R.edges():
	#	print(x,y,R[x][y])
	#print('\n')

	delta_start_time_2 = time.time()

	#
	# Search for s-t-route in R
	# Send flow and update R
	u,v,c,t = new_graph_edge
	new_graph_edge_cap = c
	st_route = True
	st_flow = 0
	# As long as it is possible to find new paths from s to t
	# and as long as we have not yet sent the amount of flow from s to t possible to send on uv
	while st_route == True and st_flow < new_graph_edge_cap:
		# Search for alternative route from s to t in R
		st_route, R = FindRoute(R,'s','t')
		print('st_route : ', st_route)
		# If there is such a route send flow 
		if st_route == True:
			R, flow_value = SendFlow(R,'s','t',(new_graph_edge_cap-st_flow))
			st_flow = st_flow + flow_value 
			print('flow sent from s to t : ', st_flow)
			print('\n')	

	#
	# Give final new Max-flow
	#

	new_max_flow = max_flow - alpha + st_flow
	print('new max flow : ', new_max_flow)
	



	delta_cost = new_max_flow - max_flow
	#print('delta cost : ', delta_cost)
	
	delta_time = delta_time + time.time() - delta_start_time_2

	return R,new_max_flow,delta_cost,delta_time	

# PROB_IMPR
# Probabilistic Improvement
# (Choose non-improving step with probability p)
def ProbImpr(p,delta_cost):
	flip = True
	non_imp_flip = False
	prob = p
	if delta_cost >= 0:
		non_imp_flip = True
		r = random.random()
		if r > prob:
			flip = False
	return flip,non_imp_flip

# SIM_AN
# Simulated Annealing
# (Choose non-improving step with probability e^(-delta_cost/temp))
def SimAn(T,s,a,delta_cost):
	flip = True
	non_imp_flip = False
	temp = T*a**(s-1)
	if delta_cost >= 0:
		non_imp_flip = True
		r = random.random()
		#print('Prob of nonimproving step : ',exp(-delta_cost/temp))
		#print('Random number, r : ',r)
		if r > exp(-delta_cost/temp):
			flip = False
	return flip,non_imp_flip


