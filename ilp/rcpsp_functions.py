#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque

class Job(object):
    __slots__ = [
          "i"       # Number
        , "es"      # Earliest start
        , "ls"      # Latest start
        , "ef"      # Earliest Finish
        , "lf"      # Latest Finish
        , "d"       # duration
        , "usage"   # [x, x]
        , "successors" # [activityX, activityX]
        , "predecessors" # [activityX, activityX]
    ]

    def __repr__(self):
        str = "("
        for x in self.__slots__:
            try:
                str += "%s=%s," % (x,self.__getattribute__(x))
            except AttributeError:
                continue
        str += ")";
        return str

# Calculate Earliest start/finish times (ES, EF), Latest Start/finish (LS,LF) times for all jobs
# See section 2 LB1 from Klein and Scholl "Computing lower bounds by destructive improvement: An application to resource-constrained project scheduling"
def criticalpath_bound(jobs):
    # First job should be a supersource and has ES and EF time 0
    jobs[1].es = 0
    jobs[1].ef = 0

    todo_forward_pass = deque(jobs[1].successors)
    while todo_forward_pass:
        j = todo_forward_pass.popleft()
        job = jobs[j]
        # Max if all predecessors already have earliest start, delay otherwise
        earliest_start = max([jobs[i].ef if hasattr(jobs[i],"es") else float("inf") for i in job.predecessors])
        if(earliest_start < float("inf")):
            job.es = earliest_start
            job.ef = earliest_start + job.d
        # Else there is still a predecessor that hasn't been calculated yet, so j will get added later again
        todo_forward_pass.extend(job.successors)

    # Last finish for terminal dummy job is equal to last start, which is equal to earliest start
    jobs[len(jobs)].ls = jobs[len(jobs)].es
    jobs[len(jobs)].lf = jobs[len(jobs)].es

    todo_backward_pass = deque(jobs[len(jobs)].predecessors)
    while todo_backward_pass:
        j = todo_backward_pass.popleft()
        job = jobs[j]

        last_finish = min([jobs[h].ls if hasattr(jobs[h],"ls") else -1 for h in job.successors])
        if(last_finish >= 0):
            job.lf = last_finish
            job.ls = last_finish - job.d
        # Else there is still a successor that hasn't been calculated yet, so j will get added later again
        todo_backward_pass.extend(job.predecessors)

    #for (i, job) in jobs.iteritems():
    #    print "%d es=%d ef=%d ls=%d lf=%d" % (i,job.es,job.ef, job.ls, job.lf)

def read_RCPSP_sm(filec):
    jobs = {}
    resource_availability = {}

    sections = filec.split("************************************************************************");

    # Precendence relations, section 4
    lines = sections[4].split("\n")[3:-1]
    for line in [line.split() for line in lines]:
        job = Job()
        job.i = int(line[0])
        job.predecessors = []
        job.successors = [int(x) for x in line[3:]]
        jobs[job.i] = job

    # Fill up predecessors
    for (i, job) in jobs.iteritems():
        for successor in job.successors:
            jobs[successor].predecessors.append(i)

    # Jobs, section 5
    lines = sections[5].split("\n")[4:-1]
    for line in [line.split() for line in lines]:
        job = jobs[int(line[0])]
        job.d = int(line[2])
        job.usage = [int(x) for x in line[3:]]

    # Resources, section 6
    resource_availability = [int(x) for x in sections[6].split("\n")[3].split()]

    return (resource_availability, jobs)
