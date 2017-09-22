"""Subsets.py

List all subsets of a given sequence

The subsets are yielded as the sequence of values
of a dynamic set; if any of these subsets needs
to be kept persistently, while listing more of them,
it should be copied to another structure.

D. Eppstein, September 2017."""

def subsets(S):
    """All subsets of sequence S."""
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
