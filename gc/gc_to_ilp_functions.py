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

def GC_to_LP_file(N,E,k,outputfile):
    objfunction = ""
    subjectto = []
    bounds = []
    integers = []

    # Variablen:
    # yi : kleur i wordt wel/niet gebruikt
    # xi_k : node i heeft kleur k wel/niet

    # Objective function: minimaliseer het aantal kleuren
    objfunction = " + ".join(["y"+str(i) for i in xrange(1,N+1)])

    # Zorg dat elke vertex precies één kleur heeft
    for i in xrange(1,N+1):
        subjectto.append(" + ".join(["x%d_%d"%(i,k) for k in xrange(1,N+1)]) + " = 1")

    # Zorg dat nodes geen kleur krijgen die niet gebruikt wordt
    for i in xrange(1,N+1):
        for k in xrange(1,N+1):
            subjectto.append("x%d_%d - y%d <= 0" % (i,k,k))

    # Zorg dat nodes die met een edge verbonden zijn niet dezelfde kleur krijgen
    for (v,w) in E:
        for k in xrange(1,N+1):
            subjectto.append("x%d_%d + x%d_%d <= 1" % (v,k,w,k))

    # Zorg dat alle variabelen 0 of 1 zijn
    for k in xrange(1,N+1):
        bounds.append("0 <= y%d <= 1" % k)
        integers.append("y%d" % k)
        for x in xrange(1,N+1):
            bounds.append("0 <= x%d_%d <= 1" % (x,k))
            integers.append("x%d_%d" % (x,k))

    return (objfunction, subjectto, bounds, integers)

def to_ilp(objfunction, subjectto, bounds, integers):
    result = "Minimize\n"
    result += "\t" + objfunction + "\n"
    result += "Subject To\n"
    c = 1
    for constraint in subjectto:
        result += "\tc%d: %s\n" % (c,constraint)
        c = c+1
    result += "Bounds\n\t"
    result += "\n\t".join(bounds)
    result += "\nIntegers\n\t"
    result += "\n\t".join(integers)
    result += "\nEnd"
    return result

def gc_string_to_ilp_file(instance, N, E, k, outputfile):
    
    (objfunction, subjectto, bounds, integers) = GC_to_LP_file(N,E,k,outputfile)
	
    outputf = open(outputfile, 'wb')
    outputf.write(to_ilp(objfunction, subjectto, bounds, integers))
    outputf.close()

# A dictgraph represents a graph as a dictionary with the neighbors of a graph as a list
def to_dictgraph(V, E):
    g = {}
    for v in V:
        g[v] = []
    for (u,w) in E:
        g[u].append(w)
        g[w].append(u)
    return g

# The highest node degree in a given graph
def highest_degree(V,E):
    g = to_dictgraph(V,E)
    return max(map(len, g.values()))

def maximum_k(V,E):
    return highest_degree(V,E)+1
