#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
from gc_to_sat_functions import *

# Aanroep: gc_to_sat_verify k problem-file solution-file

if(len(sys.argv) < 2):
    k = int(raw_input('k: '))
else:
    k = int(sys.argv[1])

if(len(sys.argv) < 3):
    problemfn = raw_input("Problem file: ");
else:
    problemfn = sys.argv[2]

if(len(sys.argv) < 4):
    solutionfn = raw_input('Solution file: ')
else:
    solutionfn = sys.argv[3]



with open(solutionfn) as solutionf:
    solution = read_DIMARCS_CNF_solution(solutionf.readlines())

colormap = SAT_solution_to_colormap(k, solution)
print repr(colormap).replace(",", ",\n")

# Read the problem file
with open(problemfn) as problemf:
    (N,M,E) = read_DIGRAPH(problemf.readlines())

valid = True

# First check: Every node has a color
if valid:
	if len(colormap) != N:
    		valid = False
    		print "Not every node has a color"

# Go through all edges and check that adjacent nodes do not have the same colors
if valid:
	for (v,w) in E:
 	   	if colormap[v] == colormap[w]:
        		valid = False
	       		print "Nodes %d and %d are adjacent and have the same color %d" % (v,w,colormap[v])

if not valid:
    print "Solution has problems"
else:
    print "Valid solution"
