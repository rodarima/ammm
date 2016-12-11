from pulp import *
import json, sys
from os import path
import math

# PARAMETERS ------------------------------------------------------------------


file_name = path.basename(__file__)
problem = file_name[:-3]

data = json.load(sys.stdin)

ALPHA = data['f']
BETA = data['c']
K = data['k']
D = data['d']
D = 3
R = data['cr']
N_AP = data['accessPoints']
V = data['posUsers']
W = data['posAccessPoints']

U = range(0, len(R))
A = range(0, N_AP)

# PRECOMPUTING ----------------------------------------------------------------

def dist(a, b):
	return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Precompute a table with all the possible distances
Z = []
for u in U:
	Zu = []
	for a in A:
		Zu.append(dist(V[u], W[a]))
	Z.append(Zu)

# VARIABLES -------------------------------------------------------------------

def matrix_var(I, J, name, minimum=0, maximum=None, kind=LpInteger):
	w = []
	for i in I:
		w_i = []
		for j in J:
			w_ij = LpVariable(name + "_{}_{}".format(i,j), minimum, maximum, kind)
			w_i.append(w_ij)
		w.append(w_i)
	return w

def vector_var(I, name, minimum=0, maximum=None, kind=LpInteger):
	w = []
	for i in I:
		w_i = LpVariable(name + "_{}".format(i), minimum, maximum, kind)
		w.append(w_i)
	return w

# The vector P, where a 1 states a router in that position
P = vector_var(A, 'P', 0, 1, LpBinary)

# The matrix C, so C_ua is 1 if the user u is connected to the router at a.
C = matrix_var(U, A, 'C', 0, 1, LpBinary)

# The cost of the router at the access point a
M = vector_var(A, "M", 0, kind=LpContinuous)

# CONSTRAINTS -----------------------------------------------------------------

# The problem
prob = LpProblem(problem, LpMinimize)

# Constraint 1
for a in A:
	prob += M[a] == ALPHA * P[a] + BETA * lpSum([C[u][a] for u in U])

# Constraint 2
for a in A:
	prob += lpSum([R[u] * C[u][a] for u in U]) <= K * P[a]

# Constraint 3
for u in U:
	prob += lpSum([C[u][a] for a in A]) == 1

# Constraint 4
for u in U:
	prob += lpSum([C[u][a] * Z[u][a] for a in A]) <= D

#for u in U:
#	apx = lpSum([C[u][a] * W[a][0] for a in A])
#	apy = lpSum([C[u][a] * W[a][1] for a in A])
#	Vx = V[u][0]
#	Vy = V[u][0]
#	prob += dist(apx, apy, Vx, Vy) <= D


# Objective function
prob += lpSum([M[a] for a in A])

# SOLVE -----------------------------------------------------------------------

# solve the problem
status = prob.solve(GLPK(msg=0, keepFiles=1, options=['--log',problem+'-pulp.log']))
print("Solver status: {}".format(LpStatus[status]))

# PRINT RESULTS ---------------------------------------------------------------

def print_matrix(M, I, J, name=None):
	if name != None:
		print("Matrix {}:".format(name))
	for i in I:
		line = []
		for j in J:
			line.append(str(value(M[i][j])))
		print("  " + "  ".join(line))

def print_fmatrix(M, I, J, name=None):
	if name != None:
		print("Matrix {}:".format(name))
	for i in I:
		line = []
		for j in J:
			line.append("{:.2f}".format(value(M[i][j])))
		print("  " + "  ".join(line))

def print_vector(V, I, name=None):
	if name != None:
		print("Vector {}:".format(name))
	line = []
	for i in I:
		line.append(str(value(V[i])))
	print("  " + "  ".join(line))

print('Cost: sum(M) = {}'.format(sum([value(m) for m in M])))
print_matrix(C, U, A, 'C')
print_vector(M, A, 'M')
print_vector(P, A, 'P')
print_vector(R, U, 'R')
print_fmatrix(Z, U, A, 'Z')

for a in A:
	if value(P[a]) == 0: continue
	resources = 0
	capacity = K
	users = []
	ds = []
	for u in U:
		if value(C[u][a]) == 1:
			resources += R[u]
			users.append(u)
			ds.append("{:.2f}".format(Z[u][a]))
	
	print("Router at {} used {}/{} by users {} at distances [{}]".format(
		a, resources, capacity, users, ", ".join(ds)))


#KD = 100
#with open('test.dot', 'w') as f:
#	f.write('graph G { overlap=true; splines=true\n')
#	minx = min(min(V[:][0]), min(W[:][0])) - 1
#	miny = min(min(V[:][1]), min(W[:][1])) - 1
#	maxx = max(max(V[:][0]), max(W[:][0])) + 2
#	maxy = max(max(V[:][1]), max(W[:][1])) + 2
#	for x in range(minx, maxx):
#		for y in range(miny, maxy):
#			f.write('  p_{}_{} [ shape = point color=gray width=0.1 pos = "{},{}!" ]\n'.format(
#				x,y,x*KD, y*KD))
#	for u in U:
#		ux = V[u][0]
#		uy = V[u][1]
#		#f.write('  u{} [ shape = point label = U{} ]\n'.format(u,u))
#		f.write('  u{} [ shape = point width=0.05 color=red label = U{} pos = "{},{}!" ]\n'.format(
#			u,u,ux*KD-9+(u*23 % 17), uy*KD+3+(u*29 % 17)))
#	for a in A:
#		ax = W[a][0]
#		ay = W[a][1]
#		f.write('  a{} [ shape = point width=0.05 label = a{} pos = "{},{}!" ]\n'.format(a,a,ax*KD+10, ay*KD))
#		#f.write('  a{} [ label = A{} ]\n'.format(a,a))
#	for u in U:
#		ux = V[u][0]
#		uy = V[u][1]
#		con = -1
#		for a in A:
#			if value(C[u][a]) == 1:
#				con = a
#				break
#		#f.write('  u{} -- a{} [label = "R{} D{:.2f}"]\n'.format(u,con,R[u], Z[u][a]))
#		f.write('  u{} -- a{} \n'.format(u,con))
#		#f.write('  u{} -- p_{}_{} \n'.format(u,ux,uy))
#	f.write('}\n')
#
#os.system('neato test.dot -n -Tpng -o test.png')
