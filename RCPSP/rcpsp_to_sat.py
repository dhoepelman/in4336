#!/usr/bin/env python
# -*- coding: utf-8 -*-

class activity:
    pass
    # i = Number
    # es = Earliest start
    # ls = Latest start
    # ef = Earliest Finish
    # lf = Latest Finish
    # d = duration

Gives the distance between two activities
def distance(a1, a2):
    if a1.i == a2.i:
        return -a1.d
    # TODO

# First group of clauses: consistency clauses
# Either you cannot start at time t, or you have to be in progress for t + d for that particular acitivity
for a in activities:
    for t in xrange(a.es, a.ls+1):
        for l in xrange(t, t+d):
            clauses.append(-s_it, u_il)

# TODO: Precendence clauses

# Make sure that every activity starts
for a in activities:
    clause = []
    for t in xrange(a.es, a.ls+1):
        clause.add(s_it)
    clauses.append(clause)

# Cover clauses. Make sure that no activities can be in progress at the same time that exceed the consumption of a available rsource