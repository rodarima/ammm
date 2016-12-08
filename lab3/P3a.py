from pulp import *
import json, sys

# PARAMETERS ------------------------------------------------------------------

nTasks = 4 
nThreads = 8 
nCPUs = 3 
nCores = 9 
 
rh = [261.27, 261.27, 560.89, 560.89, 310.51, 310.51, 105.8, 105.8]

rc = [505.67, 503.68, 701.78]
 
CK = [ 
	[1,1,1,0,0,0,0,0,0],
	[0,0,0,1,1,1,0,0,0],
	[0,0,0,0,0,0,1,1,1]
] 

assert(CK[0][1] == 1)
 
 
TH = [ 
	[1,1,0,0,0,0,0,0],
	[0,0,1,1,0,0,0,0],
	[0,0,0,0,1,1,0,0],
	[0,0,0,0,0,0,1,1]
] 

assert(TH[0][1] == 1)

problem = 'P3a'

T = range(nTasks)
C = range(nCPUs)
H = range(nThreads)
K = range(nCores)


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

# xtc binary. Equal to 1 if task t is served from computer c; 0 otherwise.
xtc = matrix_var(T, C, 'xtc', 0, 1, LpBinary)

# xhk binary. Equal to 1 if thread h is served from core k; 0 otherwise.
xhk = matrix_var(H, K, 'xhk', 0, 1, LpBinary)

# z positive real with percentage of load of the highest loaded computer.
z = LpVariable("z", 0, 1, LpContinuous)

# CONSTRAINTS -----------------------------------------------------------------

# The problem
prob = LpProblem(problem, LpMinimize)

# Constraint 1
for h in H:
	prob += lpSum([xhk[h][k] for k in K]) == 1

# Constraint 2
for t in T:
	Ht = TH[t]
	num_threads = sum(Ht)
	for c in C:
		prob += lpSum([
			lpSum([
				xhk[h][k]
				for k in K if CK[c][k] == 1
			])
			for h in H if TH[t][h] == 1 
		]) == num_threads * xtc[t][c]

# Constraint 3
for c in C:
	for k in K:
		if CK[c][k] == 1:
			prob += lpSum([rh[h] * xhk[h][k] for h in H]) <= rc[c]

# Constraint 4
for c in C:
	prob += z >= 1 / (sum(CK[c])*rc[c]) * lpSum([lpSum([rh[h] * xhk[h][k]
		for k in K if CK[c][k] == 1]) for h in H])


# Objective function
prob += z

# SOLVE -----------------------------------------------------------------------

# solve the problem
status = prob.solve(GLPK(msg=0, keepFiles=1, options=['--log',problem+'-pulp.log']))
print("Solver status: {}".format(LpStatus[status]))

# PRINT RESULTS ---------------------------------------------------------------

vxhk = [[value(x) for x in xk] for xk in xhk]
vxtc = [[value(x) for x in xc] for xc in xtc]
def print_mat(l):
	for xs in l:
		line = " ".join(map(str, xs))
		print("    {}".format(line))

print("CK")
print_mat(CK)
print("TH")
print_mat(TH)
print("x_hk")
print_mat(vxhk)
print("x_tc")
print_mat(vxtc)
print("z = {}".format(value(z)))

#rcpus = []
#for c in C:
#	rcpu = 0
#	for t in T:
#		if value(xtc[t][c]) == 1:
#			h_vec = TH[t]
#			for h in H:
#				if h_vec[h] == 1:
#					rcpu+=rh[h]
#	rcpus.append(rcpu)
#print(rcpus)
