from pulp import *
import json, sys

# PARAMETERS ------------------------------------------------------------------

# Data from the exercise

# Rate of production
r = [200, 450, 390, 250]

# Demanded units
d= [[0, 1500, 1700, 1900, 1000, 2000 , 500,  500],
	[0, 4000,  500, 1000, 3000,  500, 1000, 2000],
	[0, 2000, 2000, 3000, 2000, 2000, 2000,  500],
	[0, 3000, 2000, 2000, 1000, 1000,  500,  500]]

assert(d[0][2] == 1700)

# Cost of holding per day and unit
H = [1.5, 1.5, 2.5, 2.5]

# Current stock
cs = [5000, 7000, 9000, 8000]

problem = '9'

PRODUCTS = 4
DAYS = 7
I = range(PRODUCTS)
J = range(1, DAYS+1)
J0 = range(0, DAYS+1)
p1 = 0
p2 = 1
p3 = 2
p4 = 3

BIGNUM = 10000

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
	

# Working on product i at day j.
w = matrix_var(I, J0, 'w', kind=LpBinary)

# Quantity of products i produced at day j
q = matrix_var(I, J0, 'q', kind=LpInteger)

# Hours of production of product i at day j
h = matrix_var(I, J0, 'h', kind=LpContinuous)

# Stock of product pi at end of day j
s = matrix_var(I, J0, 's', kind=LpInteger)

# Cost of holding product i at day j
c = matrix_var(I, J0, 'c', kind=LpContinuous)

# HACK: First product produced yesterday and second product now?
pp = []
for j in J0:
	pp_j = LpVariable("pp_{}".format(j), 0, None, LpBinary)
	pp.append(pp_j)

# Total cost of stock
C = LpVariable("C", 0, None, LpContinuous)

# CONSTRAINTS -----------------------------------------------------------------

# The problem
prob = LpProblem(problem, LpMinimize)

# Each day only 1 product is produced
for j in J:
	prob += lpSum([w[i][j] for i in I]) == 1

# pp is 0 if p1 was not produced yesterday
for j in J:
	prob += pp[j] <= w[p1][j-1]

# pp is 0 if p2 is not produced today
for j in J:
	prob += pp[j] <= w[p2][j]

# pp is 1 if both p1 yesterday and p2 today
for j in J:
	prob += pp[j] >= w[p1][j-1] + w[p2][j] - 1


# At most 24h / day of production
for i in I:
	if i == p2:
		# 5 h less for product p2 after p1, HACK
		for j in J:
			prob += h[p2][j] == w[i][j] * 24 - pp[j] * 5
	else:
		for j in J:
			prob += h[i][j] == w[i][j] * 24

# No work done on day 0
for i in I:
	prob += h[i][0] == 0

# If product i is not produced (q=0), then we are not working on it (w=0)
for i in I:
	for j in J:
		prob += q[i][j] >= w[i][j]

# If working on it (w=1), then it is produced (q>0)
for i in I:
	for j in J:
		prob += q[i][j] <= w[i][j] * BIGNUM

# The quantity is hours per rate
for i in I:
	for j in J:
		prob += q[i][j] == h[i][j] * r[i]

# No quantity produced on day 0
for i in I:
	prob += q[i][0] == 0

# The current stock at day 0
for i in I:
	prob += s[i][0] == cs[i]

# All stocks at the end of the week >= 1750
for i in I:
	prob += s[i][7] >= 1750

# The stock is the previous day + produced - demanded
for i in I:
	for j in J:
		prob += s[i][j] == s[i][j-1] + q[i][j] - d[i][j]

# Cost of holding product i at end of day j
for i in I:
	for j in J:
		prob += c[i][j] == H[i] * s[i][j]

# Cost at day 0 is zero
for i in I:
	prob += c[i][0] == 0

# The last week produced product is 3
prob += w[p3][0] == 1

# Total cost of holding the products
C = lpSum([ lpSum([c[i][j] for j in J])  for i in I])

# Objective function
prob += C

# SOLVE -----------------------------------------------------------------------

# solve the problem
status = prob.solve(GLPK(msg=0, keepFiles=1, options=['--log',problem+'-pulp.log']))
print("Solver status: {}".format(LpStatus[status]))

# PRINT RESULTS ---------------------------------------------------------------

print("C = {}".format(value(C)))
print("---------------------------------------------------------------------")
for j in J0:
	work = -1
	for i in I:
		if value(w[i][j]) == 1:
			work = i
			break
	i = work
	hours = value(h[work][j])
	print("Day {}. Working for {} hours in product {}".format(
		j, hours, i+1))
	#print("Produced {} units, and demanded {}. Remaining units {}".format(
	#	value(q[i][j]), value(d[i][j]), value(s[i][j])))
	stocks = []
	holding_pay = []
	demanded = []
	produced = []
	fmt = '{:>10}'
	for i in I:
		stocks.append(fmt.format(value(s[i][j])))
		demanded.append(fmt.format(value(d[i][j])))
		produced.append(fmt.format(value(q[i][j])))
		holding_pay.append(fmt.format(value(c[i][j])))
	print("Demanded: " + ", ".join(demanded))
	print("Produced: " + ", ".join(produced))
	print("Stocks:   " + ", ".join(stocks))
	print("Holding:  " + ", ".join(holding_pay))
	print("---------------------------------------------------------------------")
