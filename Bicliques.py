"""Bicliques.py

List all maximal complete bipartite subgraphs of a given graph
Using the algorithm from

Arboricity and bipartite subgraph listing algorithms.
D. Eppstein.
Inf. Proc. Lett. 51: 207-211, 1994.
http://doi.org/10.1016/0020-0190(94)90121-X

D. Eppstein, September 2017."""

from GraphDegeneracy import degeneracyOrientation
import unittest

def subsets(S):
    S = iter(S)
    try:
        x = S.next()
    except StopIteration:
        yield set()
        return
    for T in subsets(S):
        yield T
        T.add(x)
        yield T
        T.remove(x)

def Bicliques(G):
    D = degeneracyOrientation(G)
    B = {}
    for v in G:
        for N in subsets(D[v]):     # all subsets of outgoing neighbors
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
            v = iter(F).next()      # pick a vertex
            for w in D[v]:          # try outgoing neighbors
                if adjacentToAll(w,F):
                    B[F].add(w)

    for F in list(B):
        G = B[F] = frozenset(B[F])
        if G not in B or len(B[G]) < len(F):
            B[G] = F

    output = set()
    for F in B:
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

if __name__ == "__main__":
    unittest.main()   
