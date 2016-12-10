from pulp import *
import json, sys
from os import path

# PARAMETERS ------------------------------------------------------------------


file_name = path.basename(__file__)
problem = file_name[:-3]

data = json.load(sys.stdin)

ALPHA = data['f']
BETA = data['c']
K = data['k']
R = data['cr']
N_AP = data['accessPoints']

U = range(0, len(R))
A = range(0, N_AP)


# CHECKING --------------------------------------------------------------------


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

for a in A:
	if value(P[a]) == 0: continue
	resources = 0
	capacity = K
	users = []
	for u in U:
		if value(C[u][a]) == 1:
			resources += R[u]
			users.append(u)
	
	print("Router at {} used {}/{} by users {}".format(a, resources, capacity, users))
