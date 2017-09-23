"""Bicliques.py

List all maximal complete bipartite subgraphs of a given graph
Using the algorithm from

Arboricity and bipartite subgraph listing algorithms.
D. Eppstein.
Inf. Proc. Lett. 51: 207-211, 1994.
http://doi.org/10.1016/0020-0190(94)90121-X

The running time is linear in the number of vertices of the graph
but exponential in its degeneracy.

D. Eppstein, September 2017."""

from GraphDegeneracy import degeneracyOrientation
from Subsets import subsets
import unittest

def Bicliques(G):
    D = degeneracyOrientation(G)
    B = {}
    for v in G:
        for N in subsets(D[v]):     # all subsets of outgoing neighbors
            if len(N) > 1:          # of big enough size to be interesting
                F = frozenset(N)
                if F not in B:
                    B[F] = {v}
                else:
                    B[F].add(v)

    def adjacent(v,w):
        return v in D[w] or w in D[v]
    
    def adjacentToAll(v,S):
        for w in S:
            if not adjacent(v,w):
                return False
        return True

    for F in B:                     # found incoming neighbors, now need outgoing
        if len(F) > 0:              # ignore empty and single-vertex sets
            done = set()
            for v in F:             # pick a vertex
                for w in D[v]:      # try outgoing neighbors
                    if w not in done and adjacentToAll(w,F):
                        B[F].add(w)
                done.add(w)

    for F in list(B):               # add backlinks from subsets to subsets
        G = B[F] = frozenset(B[F])  # but only to the biggest ones
        if G not in B or len(B[G]) < len(F):
            B[G] = F

    output = set()                  # keep track of what we already output
    for F in B:                     # so we only list one of (F,G) and (G,F)
        G = B[F]
        if len(F) > 1 and len(G) > 1 and (G,F) not in output:
            yield F,G
            output.add((F,G))

# ============================================================
#     If run from command line, perform unit tests
# ============================================================

class BicliqueTest(unittest.TestCase):
    def testComplete(self):
        K = {}
        for i in range(5):
            K[i] = set()
            for j in range(5):
                if i != j:
                    K[i].add(j)
        L = list(Bicliques(K))
        self.assertEqual(len(L),10)
        for F,G in L:
            self.assertEqual(frozenset((len(F),len(G))),frozenset((2,3)))

    def testGrid(self):
        G = {}
        for i in range(5):
            for j in range(5):
                G[i,j] = []
                if i < 4: G[i,j].append((i+1,j))
                if i > 0: G[i,j].append((i-1,j))
                if j < 4: G[i,j].append((i,j+1))
                if j > 0: G[i,j].append((i,j-1))
        L = list(Bicliques(G))
        self.assertEqual(len(L),16)
        for F,G in L:
            self.assertEqual(len(F),2)
            self.assertEqual(len(G),2)

if __name__ == "__main__":
    unittest.main()   
