#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os.path

# Aanroep: gc_to_sat.py k files
# k = k van k-GC
# files is een unix shell regex, bijv "*.col". Vergeet de quotes niet bij unix shells

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

def GC_to_SAT(N,E,k):
    # We have a variable for every node and color combination
    numv = N * k
    clauses = []

    # Unieke mapping van (node, kleur) naar een SAT variabele nummer
    def mapping(node, color):
        return (node-1) * k + color

    # Voeg een clause per node to zodat elke node een of meer kleuren heeft: p_11 v p_12 v p_13 etc
    for v in xrange(1,N+1):
        clause = []
        for i in xrange(1,k+1):
            clause.append(mapping(v,i))
        clauses.append(clause)

    # Voeg clauses toe zodat elke node maximaal één kleur heeft
    # For v in V
    for v in xrange(1,N+1):
        # For 1 ≤ i < j ≤ k
        for j in xrange(1,k+1):
            for i in xrange(1,j):
                # not (v heeft kleur i en v heeft kleur j)
                # => not(v heeft kleur i) of not(v heeft kleur j)
                clauses.append([-mapping(v,i), -mapping(v,j)])

    # Voeg clauses toe zodat adjacent nodes niet dezelfde kleur hebben
    for (v,w) in E:
        for i in xrange(1,k+1):
            # not (v heeft kleur i en w heeft kleur i)
            # => not(v heeft kleur i) of not(w heeft kleur i)
            clauses.append([-mapping(v, i), -mapping(w,i)])

    return (numv, clauses)

def SAT_to_DIMACS_CNF(numv, clauses):
    #header: p cnf num_variables num_clauses
    result = "p cnf %d %d\n" % (numv, len(clauses))
    for clause in clauses:
        # Clause: variable variable variable 0 \n
        result += " ".join([str(i) for i in clause]) + " 0 \n"

    return result

if(len(sys.argv) < 2):
    k = int(raw_input('k: '))
else:
    k = int(sys.argv[1])

if(len(sys.argv) < 3):
    outputdir = raw_input("Output dir: ");
else:
    outputdir = sys.argv[2]

if(len(sys.argv) < 4):
    files = raw_input('files: ')
else:
    files = sys.argv[3]



for instancefn in glob.glob(files):
    with open(instancefn) as instacef:
        (N,M,E) = read_DIGRAPH(instacef.readlines())
        (numv, clauses) = GC_to_SAT(N,E,k)
        result = SAT_to_DIMACS_CNF(numv, clauses)
        #print(result)
        outputf = open(outputdir + "/" + os.path.splitext(os.path.basename(instancefn))[0] + ".cnf", 'w')
        outputf.write(result)
        outputf.close()
