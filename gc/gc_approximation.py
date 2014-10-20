#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gc_to_sat_functions import read_DIGRAPH, to_dictgraph, maximum_k
import sys
import os
import copy

def Color_Greedy(G):
    """
    Color the graph using greedy graph algorithm
    """
    colormap = {}
    k = 1
    for (v,v_edges) in G.iteritems():
        for i in xrange(0,k):
            # Check if none of the neighbours have color i
            if not any(w in colormap and colormap[w] == i for w in v_edges):
                # None have, give color i to v
                colormap[v] = i
                break
        # If v still doesn't have a color, we need a new color
        if v not in colormap:
            colormap[v] = k
            k = k+1

    return (k,colormap)

def Color_IRC(G):
    def delete(G, v):
        # Delete the node
        del G[v]
        # Delete all edges pointing to this node
        for edges in G.values():
            edges.discard(v)

    def coalesce(G,v,w,newnode):
        # Make a new node with combined edges
        G[newnode] = G[v] | G[w]
        G[newnode].discard(v)
        G[newnode].discard(w)

        del G[v]
        del G[w]

        # Change every edge that pointed to w to v to point to newnode
        for edges in G.values():
            if v in edges:
                edges.remove(v)
                edges.add(newnode)
            if w in edges:
                edges.remove(w)
                edges.add(newnode)

    newnode = len(G)
    G2 = copy.deepcopy(G)
    colormap = {}
    stack = []
    coalesced = {}
    spilled = []
    k=1
    while True:
        # Check if there is a node with degree lower than k, and simplify the graph if there is
        restart = False
        for v in G2.keys():
            if len(G2[v]) < k:
                print "Simplify %d" % v
                stack.append(v)
                delete(G2, v)
                restart = True
            break
        if restart:
            continue
        # Check if any of the edges can be coalesced. This is the case if the number of neighbours of the new node is less than k
        for v in G2.keys():
            for w in G2[v]:
                if len(G2[v] | G2[w]) < k:
                    # Coalesce v and w
                    print "Coalesce %d and %d into %d" % (v,w,newnode)
                    stack.append(v)
                    stack.append(w)
                    coalesced[newnode] = (v,w)
                    coalesce(G2, v, w, newnode)
                    newnode = newnode + 1
                    restart = True
                    break
            if restart:
                break
        if restart:
            continue
        # Spill a node
        for v in G2.keys():
            print "Spill %d" % v
            spilled.append(v)
            delete(G2,v)
            k=k+1
            restart = True
            break
        if restart:
            continue
        # Done!
        break
    # Check that G2 does not have any more nodes
    assert not G2

    return (k, colormap)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Specify filename"
    instancefn = sys.argv[1]

    with open(instancefn, 'r') as instancef:
        (N,M,E) = read_DIGRAPH(instancef.readlines())

    id = os.path.splitext(os.path.basename(instancefn))[0]

    V = xrange(1,N+1)
    G = to_dictgraph(V,E)
    max_k = maximum_k(V,E)

    (greedy,_) = Color_Greedy(G)
    (IRC,_) = Color_IRC(G)

    print "Instance\tN\tM\tDeg+1\tGreedy\tIRC"
    print "%s\t%d\t%d\t%d\t%d\t%d" % (id[:10].ljust(10, " "), N, M, max_k, greedy,IRC)
