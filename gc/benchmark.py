#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import signal
import sys
import math
from gc_to_sat_functions import *

# Folder to keep results in
outputdir = "benchmark"
# Solution folder
solutiondir = outputdir+"/solutions"
translationdir = outputdir+"/translations"
tracedir = outputdir+"/trace"
resultfile = outputdir+"/results.csv"

# Timeout in seconds for the SAT solver
timeout = 3600

# Statistics we would like to keep
time_spent_translating = 0
time_spent_solving = 0
solution = None
lower_bound = 0             # Smallest k we know is unsatisfiable
upper_bound = float("inf")  # Smallest k we know is satisfialble
error = ""

class TimeoutException(Exception):
    pass
def timeout_handler(signum, frame):
    raise TimeoutException()
signal.signal(signal.SIGALARM, timeout_handler)

if(len(sys.argv) < 2):
    instancefn = int(raw_input('File: '))
else:
    instancefn = int(sys.argv[1])

with open(instancefn) as instancef:
    (N,M,E) = read_DIGRAPH(instancef.readlines())

    upper_bound = N

    trace = []

    # Your time starts... NOW!
    signal.alarm(timeout)

    # Binary search
    try:
        while solution is None:
            guess = math.ceil((upper_bound-lower_bound)/2.0)+lower_bound
            trace.append(guess)

            time = time.clock()
            time_spent_translating += time.clock() - time

            # We've found the smallest k! It's the upper bound
            if lower_bound == upper_bound-1:
                solution = upper_bound
    except TimeoutException:
        # MEEH, Time's up!
        pass

    # Done!
    # Cancel timeout
    signal.alarm(0)

    # Report in addition: N


