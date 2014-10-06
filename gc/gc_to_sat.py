#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os.path
from gc_to_sat_functions import *

# Aanroep: gc_to_sat.py k output-dir files
# k = k van k-GC
# files is een unix shell regex, bijv "*.col". Vergeet de quotes niet bij unix shells

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
        result = ""
        try:
            (N,M,E) = read_DIGRAPH(instacef.readlines())
            (numv, clauses) = GC_to_SAT(N,E,k)
            result = SAT_to_DIMACS_CNF(numv, clauses)
        except Exception as e:
            print "Error converting file %s" % instancefn
            print e
        #print(result)
        outputfilen = "%s/gc-%s-%d.cnf" % (outputdir, os.path.splitext(os.path.basename(instancefn))[0], k)
        outputf = open(outputfilen, 'wb')
        outputf.write(result)
        outputf.close()
        print "Converted %s to %s" % (instancefn, outputfilen)
