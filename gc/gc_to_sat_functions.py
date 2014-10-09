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

def SAT_to_DIMACS_CNF_file(N,E,k, outputfile):
    # We have a variable for every node and color combination
    numv = N * k
    # Clause per node
    numc = N
    # Clause per (edge,kleur) combinatie
    numc += len(E)*k
    # Clause per node, per kleurenpaar. Gauss' trick toepassen
    numc += N * (k * (k-1) / 2)

    with open(outputfile,'wb') as f:
        f.write("p cnf %d %d\n" % (numv, numc))

    # Voeg een clause per node to zodat elke node een of meer kleuren heeft: p_11 v p_12 v p_13 etc
    for v in xrange(1,N+1):
        clause = []
        for i in xrange(1,k+1):
            clause.append(mapping(k,v,i))
        f.write(clause_to_str(clause))

    # Voeg clauses toe zodat elke node maximaal één kleur heeft
    # For v in V
    for v in xrange(1,N+1):
        # For 1 ≤ i < j ≤ k
        for j in xrange(1,k+1):
            for i in xrange(1,j):
                # not (v heeft kleur i en v heeft kleur j)
                # => not(v heeft kleur i) of not(v heeft kleur j)
                f.write(clause_to_str([-mapping(k,v,i), -mapping(k,v,j)]))

    # Voeg clauses toe zodat adjacent nodes niet dezelfde kleur hebben
    for (v,w) in E:
        for i in xrange(1,k+1):
            # not (v heeft kleur i en w heeft kleur i)
            # => not(v heeft kleur i) of not(w heeft kleur i)
            f.write(clause_to_str([-mapping(k,v, i), -mapping(k,w,i)]))

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

def clause_to_str(clause):
    return " ".join([str(i) for i in clause]) + " 0 \n"

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

def gc_string_to_sat_file(instance, outputfile, k):
    (N,M,E) = read_DIGRAPH(instance)
    SAT_to_DIMACS_CNF_file(N,E,k,outputfile)