#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
#       rcpsp_to_ilp.py
#

import sys
import glob
import os.path
from rcpsp_functions import * 

def RCPSP_to_ILP(resources,jobs):
    objfunction = ""
    subjectto = [] 
    bounds = []
    integers = []
	
	# Variablen:
	# Ei_t : a (0-1) binair variabele dat is gelijk aan 1 
    #        desda activiteit i start aan het begin van peride t
    #        periode t zit in het interval [t, t+1)
	
    lastjob = len(jobs)
	
    # (1) Objective function: minimaliseer de executie tijd van het project
    objfunction = (" + ".join(["%d E%d_%d" % (t,lastjob,t) for t in xrange(jobs[lastjob].es, jobs[lastjob].ls+1)]))
    
	# (2) Elke job mag maar 1 keer starten
    for i in xrange(1,lastjob+1):
		    subjectto.append(" + ".join(["E%d_%d" % (i,t) for t in xrange(jobs[i].es,jobs[i].ls+1)]) + " = 1")


    # (3.1) Zorg dat job j alléén ná job i mag starten (precedence constraint/non-preemption)
    for i in xrange(1,lastjob+1):
        if len(jobs[i].successors) > 0: # Kijk alleen maar naar jobs met successor jobs
            for j in xrange(0,len(jobs[i].successors)):
                subjectto.append(" + ".join(["%d E%d_%d" % (t,jobs[i].successors[j],t) for t in xrange(jobs[jobs[i].successors[j]].es,jobs[jobs[i].successors[j]].ls+1)]) 
                                 + " - "
                                 + " - ".join(["%d E%d_%d" % (t,i,t) for t in xrange(jobs[i].es,jobs[i].ls+1)])
                                 + " >= " + str(jobs[i].d))
								 
	# Zonder heuristics te gebruiken
	tmax = 0
	for i in xrange(1,lastjob+1):						 
		tmax += jobs[i].d
	
    # (3.2) Elke job gebruikt niet meer dan het totaal beschikbare resource of type k(resource contraint)
    for k in xrange(0,len(resources)):
		for t in xrange(0,tmax+1):
			# Maak een constrains per resource en tijdseenheid
			constraint = []
			for i in xrange(1,lastjob+1):
				constraint.append(" + ".join([str(jobs[i].usage[k]) + " E%d_%d" % (i,tau) for tau in xrange(max(0,t-jobs[1].d+1),t+1)]))
					#tau = max(0,t-jobs[i].d+1)
					#subjectto.append(" + ".join(["%d E%d_%d" % (jobs[i].usage[k],i, ta) for ta in xrange(tau, t+1)])
                    #             + " <= %d" % resources[k])
			subjectto.append(" + ".join(constraint))
	
    # Zorg dat alle variabelen 0 of 1 zijn
    for n in xrange(1,lastjob+1):
        for t in xrange(jobs[n].es,jobs[n].ls+1):
            bounds.append("0 <= E%d_%d <= 1" % (n,t))
            integers.append("E%d_%d" % (n,t))
			
    # Zorg dat alle variabelen 0 of 1 zijn
    #for k in xrange(1,len(resources)+1):
    #    for x in xrange(1,lastjob+1):
    #        bounds.append("0 <= r%d_%d <= 1" % (x,k))
    #        integers.append("r%d_%d" % (x,k))

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
#	with open("../RCPSP/test-instances/test1.sm") as instancef: 
	with open(instancefn) as instancef: 
		(resources, jobs) = read_RCPSP_sm(instancef.read()) 

		# Supplement the jobs with critical path bounds 
		criticalpath_bound(jobs) 
		
		(objfunction, subjectto, bounds, integers) = RCPSP_to_ILP(resources,jobs)
		
		outputfilen = "%s/rcpsp-%s.lp" % (outputdir, os.path.splitext(os.path.basename(instancefn))[0])
		outputf = open(outputfilen, 'wb')
		outputf.write(to_ilp(objfunction, subjectto, bounds, integers))
		outputf.close()

		#test
		# print(resources)
		
		print "Converted %s to %s" % (instancefn, outputfilen)
	