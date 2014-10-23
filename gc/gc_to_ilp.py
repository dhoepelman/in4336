#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os.path
from gc_to_sat_functions import read_DIGRAPH

def GC_to_ILP(N,E):
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

if(len(sys.argv) < 2):
    outputdir = raw_input("Output dir: ");
else:
    outputdir = sys.argv[1]

if(len(sys.argv) < 3):
    files = raw_input('files: ')
else:
    files = sys.argv[2]

for instancefn in glob.glob(files):
    with open(instancefn) as instacef:
        (N,M,E) = read_DIGRAPH(instacef.readlines())
        (objfunction, subjectto, bounds, integers) = GC_to_ILP(N,E)

        outputfilen = "%s/gc-%s.lp" % (outputdir, os.path.splitext(os.path.basename(instancefn))[0])
        outputf = open(outputfilen, 'wb')
        outputf.write(to_ilp(objfunction, subjectto, bounds, integers))
        outputf.close()

        print "Converted %s to %s" % (instancefn, outputfilen)
