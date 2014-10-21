#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import signal
import sys
import math
import os
import subprocess
import time
import json
import collections
from gc_to_smt_functions import *

totaltimestart = time.time()

# Folder to keep results in
outputdir = "benchmark-smt"
# Solution folder
solutiondir = outputdir+"/solutions"
translationdir = outputdir+"/translations"
resultfile = outputdir+"/results_smt.csv"
tracedir = outputdir+"/trace"

# Timeout in seconds for the SMT solver
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
V = xrange(1,N+1)
max_k = maximum_k(V,E)
upper_bound = max_k

trace = collections.OrderedDict()

# Your time starts... NOW!
signal.alarm(timeout)

print("Starting to solve %s with N=%d,M=%d" % (instancename, N, M))

# Keep a list of processes to ensure all child processes are stopped
procs = []

try:
    while solution == -1:
        try:
            subprocess.call("killall z3")
        except:
            # Might be still Z3 processes
            pass

        # Binary search for the solution
        guess = int(math.ceil((upper_bound-lower_bound)/2.0)+lower_bound)
        trace[guess] = {}

        print("Now guessing %d within (%d,%.0f]" % (guess, lower_bound,upper_bound))
        starttime = time.time()

        id = "gc-%s-%d" % (instancename, guess)
        translationfn = "%s/%s.smt" % (translationdir, id)

        gc_string_to_smt_file(instance, translationfn, guess)

        time_this_translation = time.time() - starttime
        trace[guess]['trans'] = time_this_translation

        print("Translation complete, now starting to solve")

        starttime = time.time()

        try:
            with open("%s/%s.cnf" % (solutiondir, id), 'wb') as solutionf:
                #solverresult = subprocess.call("lingeling " + translationfn, shell=True, stdout=solutionf)
                solverprocess = subprocess.Popen("lingeling " + translationfn, shell=True, stdout=solutionf)
                procs.append(solverprocess.pid)
                solverresult = solverprocess.wait()
        finally:
            # We might be here because of TimeoutException/Keyboardinterrupt, kill the child process if it still lives
            # Polling doesn't seem to work to check if alive... Fuck it just catch the exception if it's already killed
            try:
                solverprocess.terminate()
            except:
                pass
            # Delete the translation file, since it can become several gigs
            if os.path.isfile(translationfn):
                os.remove(translationfn)

        # We're a bit screwed if the alarm signal happens exactly here before the next loop iteration, but what are the odds?
        time_this_solving = time.time() - starttime
        time_spent_solving +=  time_this_solving
        time_spent_translating += time_this_translation
        trace[guess]['solve'] = time_this_solving
        trace[guess]['this'] = time_this_translation+time_this_solving
        trace[guess]['total'] = time_spent_solving+time_spent_translating

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
            print("New bounds: (%d,%.0f) guess was %d" % (lower_bound, upper_bound, guess))
except KeyboardInterrupt:
    # User wants to cancel
    pass
except TimeoutException:
    # MEEH, Time's up!
    pass

# Done!
# Cancel timeout
signal.alarm(0)


# killall lingeling

# Report in addition: N

output = ""
if not os.path.isfile(resultfile):
    # So excel knows what separator to use
    output = "sep=,\n"
    output += "Instance,N,M,Solution,LB,UB,Highest Degree,Translation Time,Solving Time,Total Time,Time Limit,Trace\n"

time_spent_total = time.time() - totaltimestart
output += "%s,%d,%d,%d,%d,%d,%d,%.2f,%.2f,%.2f,%d,%s" %\
        (instancename,
         N,
         M,
         solution,
         lower_bound,
         upper_bound,
         max_k,
         time_spent_translating,
         time_spent_solving,
         time_spent_total,
         timeout,
         "\"%s\"" % ",".join([str(x) for x in trace.keys()])
        )

with open(resultfile, 'ab') as resultf:
	print(output, file=resultf)

if solution != -1:
    print("Done!")
    print("Took %.2fs to solve instance %s with N=%d,M=%d. Solution=%d" % (time_spent_total, instancename, N, M, solution))
else:
    print("Timeout")

with open("%s/%s.json" % (tracedir, instancename),'wb') as tracef:
    print(json.dumps(trace, indent=4), file=tracef)

try:
	subprocess.call("killall lingeling")
except:
	pass
try:
	subprocess.call("pkill lingeling")
except:
	pass

