from pulp import *
import json, sys

# PARAMETERS ------------------------------------------------------------------

# Data from the example
#nTasks = 4
#nCPUs = 3
#rt = [261.27, 560.89, 310.51, 105.80]
#rc = [505.67, 503.68, 701.78]
#rc = [600, 500]

#data = {'rt':rt, 'rc':rc}
#with open('data.json', 'w') as f:
#	json.dump(data, f)

data = json.load(sys.stdin)

rc = data['rc']
rt = data['rt']

K = int(sys.argv[1])

N = len(rt)
M = len(rc)

T = range(N)
C = range(M)

problem = 'P2d'

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
		x_tc = LpVariable("x_{}_{}".format(t,c), 0, 1, LpBinary)
		x_t.append(x_tc)
	x.append(x_t)

# Check the correct index order
#assert(str(x[1][2]) == "x_1_2")

y = []
for t in T:
	y_t = LpVariable("y_{}".format(t), 0, 1, LpBinary)
	y.append(y_t)

# Positive real with the load of the highest loaded computer.
z = LpVariable("z", 0, 1, LpContinuous)

# CONSTRAINTS -----------------------------------------------------------------

# The problem
prob = LpProblem(problem, LpMinimize)

# Constraint 1
for t in T:
	prob += lpSum([x[t][c] for c in C]) == y[t]

# Constraint 2
for c in C:
	prob += lpSum([rt[t] * x[t][c] for t in T]) <= rc[c]

# Constraint 3
for c in C:
	prob += z >= (1.0 / rc[c]) * lpSum([rt[t] * x[t][c] for t in T])

# Contraint 4
prob += lpSum([y[t] for t in T]) >= N - K


# Objective function
prob += z

# SOLVE -----------------------------------------------------------------------

# solve the problem
status = prob.solve(GLPK(msg=0, keepFiles=1, options=['--log',problem+'-pulp.log']))
print("Solver status: {}".format(LpStatus[status]))

# PRINT RESULTS ---------------------------------------------------------------

total_load = sum(rt)
total_capacity = sum(rc)
resources_available = sum(rc)

#print("Total load: {}".format(total_load))
#print("Total capacity: {}".format(total_capacity))
#print("Expected mean load: {:.3f}".format(total_load/total_capacity))

loads = [0] * N
for c in C:
	load = 0
	for t in T:
		load += rt[t] * value(x[t][c])
		#print("{}={}".format(x[t][c], value(x[t][c])))
	load = (1/rc[c]) * load
	loads[c] = load
	print("Computer {} loaded at {:.2f}%".format(c,load*100))

allowed = [0] * N
for t in T:
	allowed[t] = value(y[t])
#print("CPU{} loaded at {:.3f}".format(c, load))
#print(allowed)
#print(loads)

#print(task_in_cpu)
allowed = [0]*len(rt)
resources_used = 0
rejected_tasks = 0
for t in T:
	vt = value(y[t])
	allowed[t] = vt
	if vt == 1:
		resources_used += rt[t]
	else:
		rejected_tasks += 1
#print("CPU{} loaded at {:.3f}".format(c, load))
rejected_resources = total_load - resources_used
unused_resources = resources_available - resources_used
print("Resources used were {:.2f} of {:.2f} available".format(
	resources_used,	resources_available))
print("There were {} of {} tasks rejected with a total of {:.2f} resources".format(
	rejected_tasks, N, rejected_resources))
print("A total of {:.2f} resources were unused. K={}".format(unused_resources, value(K)))

for t in T:
	if allowed[t] == 0:
		print("Task {} with {:.2f} of resources was rejected".format(t, rt[t]))
		continue
	computer = None
	for c in C:
		if value(x[t][c]) == 1:
			computer = c
			break
	print("Task {} with {} of resources runs on computer {}".format(
		t, rt[t], computer))
