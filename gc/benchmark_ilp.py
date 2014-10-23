#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import signal
import sys
import math
import os
import subprocess
import time
import collections
from gc_to_ilp_functions import *

totaltimestart = time.time()

# Folder to keep results in
outputdir = "benchmark-ilp-new"
# Solution folder
solutiondir = outputdir+"/solutions"
translationdir = outputdir+"/translations"
resultfile = outputdir+"/results_ilp.csv"
tracedir = outputdir+"/trace"

# Timeout in seconds for the ILP solver
timeout = 1800

# Statistics we would like to keep
instancename = ""
time_spent_translating = 0
time_spent_solving = 0
solution = -1
lower_bound = 0             # Smallest k we know is unsatisfiable
upper_bound = float("inf")  # Smallest k we know is satisfialble

class TimeoutException(Exception):
    pass
def timeout_handler(signum, frame):
    raise TimeoutException()
signal.signal(signal.SIGALRM, timeout_handler)

if(len(sys.argv) < 2):
    instancefn = raw_input('File: ')
else:
    instancefn = sys.argv[1]

instancename = os.path.splitext(os.path.basename(instancefn))[0]
with open(instancefn) as instancef:
    instance = instancef.readlines()

(N,M,E) = read_DIGRAPH(instance)

max_k = maximum_k(xrange(1,N+1),E)
upper_bound = min(N, max_k)

trace = collections.OrderedDict()

# Your time starts... NOW!
signal.alarm(timeout)

print("Starting to solve %s with N=%d,M=%d" % (instancename, N, M))

try:
    starttime = time.time()

    id = "gc-%s" % instancename
    translationfn = "%s/%s.lp" % (translationdir, id)
    resultfn = "%s/%s.sol" % (solutiondir, id)

    try:
        gc_string_to_ilp_file(instance,N,E,upper_bound,translationfn)
        time_this_translation = time.time() - starttime
        #trace[guess]['trans'] = time_this_translation

        print("Translation complete, now starting to solve")

        starttime = time.time()

        try:
            solverresult = subprocess.call("gurobi_cl ResultFile="+resultfn+" "+translationfn, shell=True)
        finally:
            try:
                subprocess.call("killall gurobi_cl")
            except:
                pass

        with open(resultfn, 'r') as resultf:
            solution = int(resultf.readline().split("=")[1])

        # We're a bit screwed if the alarm signal happens exactly here before the next loop iteration, but what are the odds?
        time_this_solving = time.time() - starttime
        time_spent_solving +=  time_this_solving
        time_spent_translating += time_this_translation

#        print("Found solution: %d" % solution)
#            else:
#                print("New bounds: (%d,%.0f guess was %d" % (lower_bound, upper_bound, guess))
	timeout = False
    finally:
        # Delete the translation file, since it can become several gigs
        if os.path.isfile(translationfn):
            os.remove(translationfn)

except KeyboardInterrupt:
    # User wants to cancel
    solution = -1
    pass
except TimeoutException:
    # MEEH, Time's up!
    timeout = True
    solution = -1
    pass

# Done!
# Cancel timeout
signal.alarm(0)

# Report in addition: N

output = ""
if not os.path.isfile(resultfile):
    # So excel knows what separator to use
    output = "sep=,\n"
    output += "Instance,N,M,Max K,Solution,Translation Time,Solving Time,Total Time,Time Limit,Trace\n"

time_spent_total = time.time() - totaltimestart
output += "%s,%d,%d,%d,%d,%.2f,%.2f,%.2f,%d" %\
        (instancename,
         N,
         M,
         max_k,
         solution,
         time_spent_translating,
         time_spent_solving,
         time_spent_total,
         timeout
        )

with open(resultfile, 'ab') as resultf:
	print(output, file=resultf)

if timeout == False:
    print("Done!")
    print("Took %.2fs to solve instance %s with N=%d,M=%d. Solution=%d" % (time_spent_total, instancename, N, M, solution))
else:
    print("Timeout")

try:
	subprocess.call("killall -9 gurobi_cl")
except:
	pass
try:
	subprocess.call("pkill -9 gurobi_cl")
except:
	pass
