
"""Utilities for dealing with iterators and such.
"""

def interlace(x, i):
    """interlace(x, i) -> i0, x, i1, x, ..., x, iN
    """
    i = iter(i)
    try:
        yield i.next()
    except StopIteration:
        return
    for e in i:
        yield x
        yield e
