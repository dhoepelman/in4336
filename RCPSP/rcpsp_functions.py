#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Activity(object):
    __slots__ = [
          "i"       # Number
        , "es"      # Earliest start
        , "ls"      # Latest start
        , "ef"      # Earliest Finish
        , "lf"      # Latest Finish
        , "d"       # duration
        , "usage"   # [x, x]
        , "successors" # [activityX, activityX]
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


# Floyd-Warshall python implementation, taken from http://jlmedina123.wordpress.com/2014/05/17/floyd-warshall-algorithm-in-python/
def floydwarshall(graph):
    # Initialize dist and pred:
    # copy graph into dist, but add infinite where there is
    # no edge, and 0 in the diagonal
    dist = {}
    pred = {}
    for u in graph:
        dist[u] = {}
        pred[u] = {}
        for v in graph:
            dist[u][v] = 1000
            pred[u][v] = -1
        dist[u][u] = 0
        for neighbor in graph[u]:
            dist[u][neighbor] = graph[u][neighbor]
            pred[u][neighbor] = u

    for t in graph:
        # given dist u to v, check if path u - t - v is shorter
        for u in graph:
            for v in graph:
                newdist = dist[u][t] + dist[t][v]
                if newdist < dist[u][v]:
                    dist[u][v] = newdist
                    pred[u][v] = pred[t][v] # route new path through t

    return dist, pred


def read_RCPSP_sm(filec):
    jobs = {}
    resource_availability = {}

    sections = filec.split("************************************************************************");

    # Precendence relations, section 4
    lines = sections[4].split("\n")[3:-1]
    for line in [line.split() for line in lines]:
        job = Activity()
        job.i = int(line[0])
        job.successors = [int(x) for x in line[3:]]
        jobs[job.i] = job

    # Jobs, section 5
    lines = sections[5].split("\n")[4:-1]
    for line in [line.split() for line in lines]:
        job = jobs[int(line[0])]
        job.d = int(line[2])
        job.usage = [int(x) for x in line[3:]]

    # Resources, section 6
    resource_availability = [int(x) for x in sections[6].split("\n")[3].split()]

    return (resource_availability, jobs)