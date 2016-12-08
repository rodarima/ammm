from pulp import *

# PARAMETERS ------------------------------------------------------------------

# Data from the example
#nTasks = 4
#nCPUs = 3
rt = [261.27, 560.89, 310.51, 105.80]
rc = [505.67, 503.68, 701.78]
#rc = [600, 500]

T = range(len(rt))
C = range(len(rc))

# CHECKING --------------------------------------------------------------------

if sum(rt) > sum(rc):
	print("Not enough computer resources")
	exit(1)

# VARIABLES -------------------------------------------------------------------

# The percentaje of resources by task t that are served from computer c, 
# called x_tc = x[t][c]
x = []
for t in T:
	x_t = []
	for c in C:
		x_tc = LpVariable("x_{}_{}".format(t,c), 0, 1, LpContinuous)
		x_t.append(x_tc)
	x.append(x_t)

# Check the correct index order
#assert(str(x[1][2]) == "x_1_2")

# Positive real with the load of the highest loaded computer.
z = LpVariable("z", 0, 1, LpContinuous)

# CONSTRAINTS -----------------------------------------------------------------

# The problem
prob = LpProblem("problem", LpMinimize)

# Constraint 1
for t in T:
	prob += lpSum([x[t][c] for c in C]) == 1.00

# Constraint 2
for c in C:
	prob += lpSum([rt[t] * x[t][c] for t in T]) <= rc[c]

# Constraint 3
for c in C:
	prob += z >= (1.0 / rc[c]) * lpSum([rt[t] * x[t][c] for t in T])

# Objective function
prob += z

# SOLVE -----------------------------------------------------------------------

# solve the problem
status = prob.solve(GLPK(msg=0))
print("Solver status: {}".format(LpStatus[status]))

# PRINT RESULTS ---------------------------------------------------------------

total_load = sum(rt)
total_capacity = sum(rc)

print("Total load: {}".format(total_load))
print("Total capacity: {}".format(total_capacity))
#print("Expected mean load: {:.3f}".format(total_load/total_capacity))

for c in C:
	load = 0
	for t in T:
		load += rt[t] * value(x[t][c])
	load = (1/rc[c]) * load
	print("CPU{} loaded at {:.3f}".format(c, load))
