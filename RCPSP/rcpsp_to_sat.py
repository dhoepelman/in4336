#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rcpsp_functions import *


'''
# Gives the distance between two activities
def distance(a1, a2):
    if a1.i == a2.i:
        return -a1.d
    # TODO


# TODO: Precendence clauses



# Cover clauses. Make sure that no activities can be in progress at the same time that exceed the consumption of a available rsource
'''

with open("test-instances/test1.sm") as instancef:
    (resources, jobs) = read_RCPSP_sm(instancef.read())

    # Supplement the jobs with critical path bounds
    criticalpath_bound(jobs)

    T = 100

    # Compute the shortest distances between each
    # Give the edges the weight of the negative duration. Thus the shorted path coincides with the longest path in the original graph
    # Note: The longest-path problem is NP-Hard in general, this works only for a DAG like the precedence graph in RCPSP.
    #       In a normal graph this will create cycles of negative length, thus rendering Floyd-Warshall useless
    #graph = {}
    #for job in jobs.values():
    #    graph[job.i] = {}
    #    for suc in job.successors:
    #        graph[job.i][suc] = -job.d
    #print repr(floydwarshall(graph)).replace("}, ","},\n")

    # Define all the necessary boolean variables
    mapping = {}
    cur = 1
    for (i,job) in jobs.iteritems():
        # Start variables
        for t in xrange(job.es, job.ls+1):
            mapping[('s',i,t)] = cur
            cur = cur+1
        # Process variables
        for t in xrange(job.es, job.lf+1):
            mapping[('u',i,t)] = cur
            cur = cur+1

    # The clauses
    clauses = []

    # First group of clauses: consistency clauses
    # Either you cannot start at time t, or you have to be in progress for t + d for that particular acitivity
    for (i,job) in jobs.iteritems():
        for t in xrange(job.es, job.ls+1):
            for l in xrange(t, t+job.d):
                clauses.append([-mapping[('s',i,t)],mapping[('u',i,l)]])

    # Second group: precedence clauses
    for (i, job) in jobs.iteritems():
        for j in job.successors:
            job_pred = jobs[j]
            generic_part = [mapping[('s',j,l)] for l in xrange(job_pred.es, job.es - job_pred.d + 1)]
            # If i starts at t, all its predecessors start early enough to allow this start of i
            for t in xrange(job.es, job.ls+1):
                clause = [-mapping[('s',i,t)]]
                clause.extend(generic_part)
                clauses.append(clause)

    # Third group: Make sure that every activity starts
    for (i,job) in jobs.iteritems():
        clauses.append([mapping[('s',i,t)] for t in xrange(job.es, job.ls+1)])

    # The dreaded exponential clauses.
    # Go trough all fucking combinations of jobs (2^|V| !!!)
    to_check = jobs.keys()
    # Don't include the supersource and supersink
    to_check.remove(1)
    to_check.remove(len(jobs))

    def consumes_too_much_resources(set_of_jobs):
        for (i,limit) in enumerate(resources):
            if sum([jobs[job].usage[i] for job in set_of_jobs]) > limit:
                #print "%s: %d > %d" % (set_of_jobs, sum([jobs[job].usage[i] for job in set_of_jobs]), limit)
                return True
        return False

    # Precondition: set of jobs consumes too much resources
    def is_minimal_cover(set_of_jobs):
        for job in set_of_jobs:
            if consumes_too_much_resources(set_of_jobs - frozenset([job])):
                return False

        return True

    def add_minimal_cover_clause(set_of_jobs):
        for t in xrange(0, T):
            clause = []
            for i in set_of_jobs:
                # There is an error in the paper. t in [0,T-1] but u_it is defined for a much narrower range of t
                if ('u',i,t) in mapping:
                    clause.append(-mapping[('u',i,t)])
            clauses.append(clause)

    def find_all_minimal_covers(set_of_jobs):
        if(consumes_too_much_resources(set_of_jobs)):
            if(is_minimal_cover(set_of_jobs)):
                add_minimal_cover_clause(set_of_jobs)
            else:
                for job in set_of_jobs:
                    find_all_minimal_covers(set_of_jobs - frozenset([job]))


    find_all_minimal_covers(frozenset(jobs.keys()))

    print clauses








