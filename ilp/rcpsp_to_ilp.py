#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
 
from rcpsp_functions import * 

def RCPSP_o_ILP(N,E):
	objfunction = "" 
    subjectto = [] 
    bounds = [] 
    integers = [] 
	
	# Variablen:
	
	# Objective function: minimalize the makespan/project completion time
	objfunction = " + ".join([])

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


with open("test-instances/test1.sm") as instancef: 
    (resources, jobs) = read_RCPSP_sm(instancef.read()) 

    # Supplement the jobs with critical path bounds 
    criticalpath_bound(jobs) 

	