#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os.path
from gc_to_smt_functions import *

# Z3 is a state-of-the-art theorem solver
# A Z3 script is a sequence of commands

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
        instance = instacef.readlines()
        (N,M,E) = read_DIGRAPH(instance)
        
        V = xrange(1,N+1)
        max_k = maximum_k(V,E)
        upper_bound = max_k
        
        outputfilen = "%s/gc-%s.smt" % (outputdir, os.path.splitext(os.path.basename(instancefn))[0])
        
        gc_string_to_smt_file(instance,outputfilen,upper_bound)

        print("Converted %s to %s") % (instancefn, outputfilen)
