"""DFS.py

Algorithms for depth first search in Python.
We need to search iteratively rather than recursively in
order to avoid Python's low recursion limit.

D. Eppstein, July 2004.
"""

from sets import Set

# Types of edges in DFS traversal.
# The numerical values are used in DepthFirstSearcher, change with care.
forward = 1     # traversing edge (v,w) from v to w
reverse = -1    # returning backwards on (v,w) from w to v
nontree = 0     # edge (v,w) is not part of the DFS tree

def search(G):
    """
    Generate sequence of triples (v,w,edgetype) for DFS of graph G.
    The subsequence for each root of each tree in the DFS forest starts
    with (root,root,forward) and ends with (root,root,reverse).
    """
    visited = Set()
    for v in G:
        if v not in visited:
            yield v,v,forward
            visited.add(v)
            stack = [(v,iter(G[v]))]
            while stack:
                parent,children = stack[-1]
                try:
                    child = children.next()
                    if child in visited:
                        yield parent,child,nontree
                    else:
                        yield parent,child,forward
                        visited.add(child)
                        stack.append((child,iter(G[child])))
                except StopIteration:
                    stack.pop()
                    if stack:
                        yield stack[-1][0],parent,reverse
            yield v,v,reverse

def preorder(G):
    """Generate all vertices of graph G in depth-first preorder."""
    for v,w,edgetype in search(G):
        if edgetype is forward:
            yield w

def postorder(G):
    """Generate all vertices of graph G in depth-first postorder."""
    for v,w,edgetype in search(G):
        if edgetype is reverse:
            yield w

class Searcher:
    """
    Handler for performing general depth first searches of graphs.
    Some or all of the routines preorder, postorder, and backedge
    should be shadowed in order to make the search do something useful.
    """

    def preorder(self,parent,child):
        """
        Called when DFS visits child, before visiting all grandchildren.
        Parent==child when child is the root of each DFS tree.
        """
        pass

    def postorder(self,parent,child):
        """
        Called when DFS visits child, after visiting all grandchildren.
        Parent==child when child is the root of each DFS tree.
        """
        pass

    def backedge(self,source,destination):
        """Called when DFS discovers an edge to a non-child."""
        pass

    def __init__(self,G):
        """Perform a depth first search of graph G."""
        dispatch = [self.backedge,self.preorder,self.postorder]
        for v,w,edgetype in search(G):
            dispatch[edgetype](v,w)
