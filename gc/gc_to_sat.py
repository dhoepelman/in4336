#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import glob
import os.path
from gc_to_sat_functions import *


# Aanroep: gc_to_sat.py k output-dir files
# Voorbeeld: gc_to_sat.py 100 . te-kleueren-graaf.sol
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
    filen = raw_input('file: ')
else:
    filen = sys.argv[3]

with open(filen) as instacef:
    result = ""
    try:
        (N,M,result) = gc_string_to_sat_string(instacef.readlines(), k)

        outputfilen = "%s/gc-%s-%d.cnf" % (outputdir, os.path.splitext(os.path.basename(filen))[0], k)
        with open(outputfilen, 'wb') as outputfile:
            print(result, file=outputfile)
        print("Converted %s to %s" % (filen, outputfilen))
    except Exception as e:
        print("Error converting file %s" % filen)
        print(e)