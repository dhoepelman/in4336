from gc_to_sat_functions import  to_dictgraph
from copy import copy

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
    def to_dictsetgraph(G):
        G2 = {}
        for v,vedges in G.iteritems:
            G2[v] = set(vedges)
        return G2

    def delete(G, v):
        # Delete the node
        del G[v]
        # Delete all edges pointing to this node
        for edges in G.values():
            edges.remove(v)

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
    G2 = to_dictsetgraph(G)
    colormap = {}
    stack = []
    coalesced = {}
    spilled = []
    k=1
    while True:
        # Check if there is a node with degree lower than k, and simplify the graph if there is
        for v in G2.keys():
            if len(G2[v]) < k:
                stack.push(v)
                delete(G2, v)
            continue
        # Check if any of the edges can be coalesced. This is the case if the number of neighbours of the new node is less than k
        for v in G2.keys():
            for w in G2[v]:
                if len(G2[v] | G2[w]) < k:
                    # Coalesce v and w
                    stack.push(v)
                    stack.push(w)
                    coalesced[newnode] = (v,w)
                    coalesce(G2, v, w, newnode)
                    newnode = newnode + 1
                    continue
        # Spill a node
        for v in G2.keys():
            spilled.add(v)
            delete(G2,v)
            k=k+1
            continue
        # Done!
        break
    # Check that G2 does not have any more nodes
    assert not G2

    return (k, colormap)