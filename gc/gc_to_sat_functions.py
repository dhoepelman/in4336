#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read_DIGRAPH(lines):
    # List of edges
    E = []
    for line in lines:
        vals = line.split(" ")
        if vals[0] == 'p':
            # Number of nodes
            N = int(vals[2])
            # Number of edges
            M = int(vals[3])
        elif vals[0] == 'e':
            # Add this edge
            E.append((int(vals[1]), int(vals[2])))
    return (N,M,E)

'''
Eigenschappen van onze vertaling:
variabelen: N * k

clausules = M*k + N * (k+1)

Grootte clausulen:

Elke node heeft minimaal één kleur: p_1,1 p_1,2 p_1,3
n : k

# Elke node heeft maximaal één kleur
# niet(p1,1 en p1,2)
# niet(p1,2 en p1,3)
N * k^2 : 2

# De nodes van een edge hebben niet dezelfde kleur
# Voor edge (1,2)
# niet(p1,1 en p2,1)
# niet(p1,2 en p2,2)
M * k : 2
'''

def GC_to_SAT(N,E,k):
    # We have a variable for every node and color combination
    numv = N * k
    clauses = []

    # Voeg een clause per node to zodat elke node een of meer kleuren heeft: p_11 v p_12 v p_13 etc
    for v in xrange(1,N+1):
        clause = []
        for i in xrange(1,k+1):
            clause.append(mapping(k,v,i))
        clauses.append(clause)

    # Voeg clauses toe zodat elke node maximaal één kleur heeft
    # For v in V
    for v in xrange(1,N+1):
        # For 1 ≤ i < j ≤ k
        for j in xrange(1,k+1):
            for i in xrange(1,j):
                # not (v heeft kleur i en v heeft kleur j)
                # => not(v heeft kleur i) of not(v heeft kleur j)
                clauses.append([-mapping(k,v,i), -mapping(k,v,j)])

    # Voeg clauses toe zodat adjacent nodes niet dezelfde kleur hebben
    for (v,w) in E:
        for i in xrange(1,k+1):
            # not (v heeft kleur i en w heeft kleur i)
            # => not(v heeft kleur i) of not(w heeft kleur i)
            clauses.append([-mapping(k,v, i), -mapping(k,w,i)])

    return (numv, clauses)

def mapping(k, node, color):
    # Unieke mapping van (node, kleur) naar een SAT variabele nummer
    return (node-1) * k + color

# Translate a mapped sat variable back to the GC (node, color) combination
# Reverse of mapping = (node-1) * k + color
def reversemapping(k, mapping):
    color = mapping % k
    if color == 0:  # Colour is in [1,k]
        color = k
    # (node-1) * k = mapping - color
    # node = (mapping-color)/k + 1
    node = (mapping - color) / k + 1
    return (node, color)

def SAT_to_DIMACS_CNF(numv, clauses):
    #header: p cnf num_variables num_clauses
    result = "p cnf %d %d\n" % (numv, len(clauses))
    for clause in clauses:
        # Clause: variable variable variable 0 \n
        result += " ".join([str(i) for i in clause]) + " 0 \n"

    return result

def read_DIMARCS_CNF_solution(lines):
    solution = {}

    for line in lines:
        # Solution line example: v 1 -2 3 -4 5 6 0
        if len(line) > 0 and line.strip()[0] == 'v':
            varz = line.split(" ")[1:]
            for v in varz:
                v = v.strip()
                value = v[0] != '-'
                vn = int(v.lstrip('-'))
                # The very last sign is a zero to indicate the end of the solution
                if vn != 0:
                    solution[vn] = value

    return solution

def SAT_solution_to_colormap(k, solution):
    assignment = {}

    for variable, value in solution.iteritems():
        if value:
            (node, color) = reversemapping(k, variable)
            assignment[node] = color
    return assignment