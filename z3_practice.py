from platform import java_ver
from z3 import *

x = Int('x1')
y = Int('y1')
solve(x > 2, y < 10, x + 2*y == 7) # prints to stdout
print(type(solve(x > 2, y < 10))) # nonetype 

# Int('x') creates an integer variable in Z3 named x
# solve functions solves a system of constraints!

# example: 2 variables, x and y, and 3 constraints
# uses = for assignment, == for comparison

print('------ Z3: Simplify Expressions ------')

x = Int('x')
y = Int('y')

print(type(x)) # ArithRef 
print(type(x + y)) # ArithRef
print(type(simplify(x + y + 2*x + 3))) # ArithRef
print(type(simplify(x < y + x + 2))) # BoolRef
print(type(simplify(And(x < y, x > y)))) # BoolRef (takes in 2 BoolRefs)
print(simplify(x < y + x + 2))
print(simplify(And(x + 1 >= 3, x**2 + x**2 + y**2 + 2 >= 5)))

print('------ Z3: Display Information ------')
print(x**2 + y**2 >= 1)
print('skip this for now')

print('------ Z3: Traversing Expressions ------')
n = x + y >= 3
print(type(n)) # BoolRef
print("num args: ", n.num_args())
print("children: ", n.children())
print("1st child: ", n.arg(0)) # children are ArithRef
print("1st child type: ", type(n.arg(0)))
print("2nd child: ", n.arg(1))
print("operator: ", n.decl()) # type: FuncDeclRef
print(type(n.decl()))
print("op name: ", n.decl().name()) # type: str
print(type(n.decl().name()))

# Z3 can solve nonlinear polynomial constraints
# procedure Real('x') creates real variable x
# set_option() - used to configure Z3 environment

print('------ Z3: Number Types ------')
print(type(1/3)) # float
print(RealVal(1)/3)
print(type(RealVal(1)/3)) # z3.z3.ArithRef
print(type(Q(1,3))) # rational number, RatNumRef
print(type(Q(1,3) + 0.25)) # ArithRef
print(type(Q(1,3) + 1/3)) # ArithRef
print(type(Real('x') + "1/3")) # ArithRef

# rational numbers in decimal notation
x = Real('x')
solve(3*x == 1)
set_option(rational_to_decimal=True) # decimal notation
solve(3*x == 1)
set_option(precision=30)
solve(3*x == 1)

print('------ Z3: Boolean Logic ------')
p = Bool('p')
q = Bool('q')
r = Bool('r')
print(type(r)) # BoolRef
solve(Implies(p, q), r == Not(q), Or(Not(p), r)) # issues a satisfying assignment

print('------ Z3: Solvers ------')
x = Int('x')
y = Int('y')

s = Solver()
print(s)
print(type(s)) # Solver

s.add(x > 10, y == x + 2)
print(s)
print("Solving constraints in the solver s ...")
print(s.check())
print(type(s.check())) # CheckSatResult

print("Create a new scope...")
s.push()
s.add(y < 11)
print(s)
print(s.check())

print("Restoring state...")
s.pop()
print(s)
print("Solving restored set of constraints...")
print(s.check())

# use add() to "assert" constraints into the solver
# check() solves the assorted constraints
# result is sat if solution is found, unsat if not
# solver fails when unknown is returned

# each solver maintains a stack of assertions
# pop removes any assertion performed between it and the matching push
# the check method always operates on the content of solver assertion stack

print('------ Z3: Performance Statistics ------')
x = Real('x')
y = Real('y')
s = Solver()

# traverse constraints asserted into a solver, collect performance stats
print(type(x > 1)) # BoolRef
s.add(x > 1, y > 1, Or(x + y > 3, x - y < 2))
for c in s.assertions():
    # print(type(c)) # BoolRef
    print(c)

print(s.check())
print("Statistics for the last check method call...")
print(type(s.statistics())) # staistics class

# traversing statistics
for k, v in s.statistics():
    #print(type(k)) # str
    #print(type(v)) # int or float ... ?
    print("%s : %s" % (k, v))

print('------ Z3: Satisfiable Model ------')
x, y, z = Reals('x y z')
s = Solver()
s.add(x > 1, y > 1, x + y > 3, z - x < 10)
print(s.check())

m = s.model() # only defined if sat after s.check()
print("x = %s" % m[x]) # convert Ref value of x to string

print(type(m.decls()[0])) # list of FuncDeclRef, each one is unknown variable in our SMT formula

print("traversing model...")
for d in m.decls():
    #print(type(d.name())) # str
    #print(type(m[d])) # RatNumRef
    print("%s = %s" % (d.name(), m[d]))

print('------ Z3: Bitvectors ------')
x = BitVec('x', 16)
y = BitVec('y', 16)
print(type(x)) # BitVecRef
print(x + 2)
print((x + 2).sexpr())
print(type(x+2)) # BitVecRef
print(simplify(x + y - 1)) # -1 is equal to 65535 for 16-bit integers

# Create bit-vector constants
a = BitVecVal(-1, 16)
b = BitVecVal(65535, 16)
print(type(a)) # BitVecNumRef
print(simplify(a == b)) # true
print(type(a == b)) # BoolRef

# no distinction between signed and unsigned bit-vectors as numbers
# rather, special signed and unsigned versinos of arithmetical operations
x, y = BitVecs('x y', 32)
solve(LShR(x, 2) == 3)
solve(x << 2 == 3)
solve(x << 2 == 24)

print('------ Z3: Functions ------')
x = Int('x')
y = Int('y')
f = Function('f', IntSort(), IntSort())
solve(f(f(x)) > x, f(x) == y, x != y)

# Evaluate expressions in the model for a system of constraints
x = Int('x')
y = Int('y')
f = Function('f', IntSort(), IntSort())
s = Solver()
s.add(f(f(x)) == x, f(x) == y, x != y)
print(s.check())
m = s.model()
print("f(f(x)) =", m.evaluate(f(f(1))))
print("f(x)    =", m.evaluate(f(x + 1)))

print('------ Z3: Satisfiability and Validity ------')
p, q = Bools('p q')
demorgan = And(p, q) == Not(Or(Not(p), Not(q)))
print(demorgan)

def prove(f):
    s = Solver()
    s.add(Not(f))
    # f is valid if not f is unsat
    # not f is valid if f is unsat
    # if f is sat then not f is invalid
    if s.check() == unsat: # dereference global variable
        print("proved")
    else:
        print("failed to prove")

print("Proving demorgan...")
print(type(unsat)) # CheckSatResult
prove(demorgan)

# F(a, b) is valid, then Not(F) is always false, and Not(F) is unsatisfiable
# F is valid precisely when Not(F) is unsatisfiable
# if F(a, b) is satisfiable, Not(F) is invalid (contrapositiveprov of : (if Not(F) is valid, then F is unsatisfiable)

print('------ Z3: List Comprehensions ------')
X = [Int('x%s' % i) for i in range(5)]
Y = [Int('y%s' % i) for i in range(5)]
print(X)

# Create a list containing X[i] + Y[i]
X_plus_Y = [X[i] + Y[i] for i in range(5)]
print(X_plus_Y)
print(type(X_plus_Y[0])) # def ArithRef
X_plus_Y_add = [X_plus_Y[i] == i for i in range(5)]

X_gt_Y = [X[i] > Y[i] for i in range(5)]
print(X_gt_Y)
print(And(X_gt_Y)) # takes in a list
solve(And(X_gt_Y), And(X_plus_Y_add))
solve(3 == 3, 4 == 4) # solve can take a list as well
solve(And(3 == 3, 4 == 4))

X = [[Int("x_%s_%s" % (i+1, j+1)) for i in range(3) for j in range(3)]]
print(X)
pp(X)

b = Bool('p')
print(type(b)) # BoolRef
print(type(x + 4 == 5)) # BoolRef

# functions
X = IntVector('x', 5)
Y = RealVector('y', 5)
P = BoolVector('p', 5)
print(X)
print(Y)
print(type(P)) # list
print([y**2 for y in Y]) # list 
print(type(Sum([y**2 for y in Y]))) # ArtihRef

print('------ Z3: Evaluation ------')
x = Int('x')
y = Int('y')

s = Solver()
s.add(x + y == 4)
s.check()
m = s.model()
print(type(m.evaluate(x)), m.evaluate(y))

print('------ Z3: Tactics ------')
x, y = Reals('x y')
g = Goal()
g.add(x > 0, y > 0, x == y + 2)
print(g)

t1 = Tactic('simplify')
t2 = Tactic('solve-eqs')
t = Then(t1, t2)
print(t2(g))
print(type(t(g))) # ApplyResult
print(type(g)) # Goal

# Split clause splits a clause OR(f_1, ..., f_n) and split it into n subgoals
x, y = Reals('x y')
g = Goal()
g.add(Or(x < 0, x > 0), x == y + 1, y < 0)

t = Tactic('split-clause')
r = t(g)
print("r:", r)
for g in r:
    print(g)

