#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import signal
import sys
import math
import os
import subprocess
import time
from gc_to_sat_functions import *

totaltimestart = time.clock()

# Folder to keep results in
outputdir = "benchmark"
# Solution folder
solutiondir = outputdir+"/solutions"
translationdir = outputdir+"/translations"
resultfile = outputdir+"/results_sat.csv"

# Timeout in seconds for the SAT solver
timeout = 3600

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

(N,M,_) = read_DIGRAPH(instance)

upper_bound = N

trace = []

# Your time starts... NOW!
signal.alarm(timeout)

try:
    while solution == -1:
        # Binary search for the solution
        guess = int(math.ceil((upper_bound-lower_bound)/2.0)+lower_bound)
        trace.append(guess)

        starttime = time.clock()

        id = "gc-%s-%d" % (instancename, guess)
        with open("%s/%s.cnf" % (translationdir, id), 'wb') as translationf:
            print(gc_string_to_sat_string(instance, guess), file = translationf)

        time_this_translation = starttime.clock() - starttime
        starttime = time.clock()

        with open("%s/%s.cnf" % (solutiondir, id), 'wb') as solutionf:
            solverresult = subprocess.call(["lingeling",translationf], shell=True)


        # We're a bit screwed if the alarm signal happens exactly here before the next loop iteration, but what are the odds?
        time_spent_solving += time.clock() - starttime
        time_spent_translating += time_this_translation

        if solverresult == 10:
            # Satisfiable
            upper_bound = guess
        elif solverresult == 20:
            # Unsatisfiable
            lower_bound = guess

        if lower_bound == upper_bound-1:
            # We've found the smallest k! It's the upper bound
            solution = upper_bound
            print("Found solution: %d" % solution)
        else:
            print("New bounds: (%d,%d] guess was %d" % (lower_bound, upper_bound, guess))

except TimeoutException:
    # MEEH, Time's up!
    pass

# Done!
# Cancel timeout
signal.alarm(0)

# Report in addition: N

output = ""
if not os.path.isfile(resultfile):
    # So excel knows what separator to use
    output = "sep=,\n"
    output += "Instance,N,M,Solution,LB,UB,Translation Time,Solving Time,Total Time,Time Limit,Trace\n"

output += "%s,%d,%d,%d,%d,%d,%d,%d,%d,%.2f,%.2f,%.2f,%s\n" %\
        (instancename,
         N,
         M,
         solution,
         lower_bound,
         upper_bound,
         time_spent_translating,
         time_spent_solving,
         starttime.clock() - totaltimestart,
         timeout,
         "\"%s\"" % ",".join([str(x) for x in trace])
        )
