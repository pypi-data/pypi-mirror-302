"""
Module docstring.

>>> 5
5
"""

def f():
    """
    Inner docstring.

    >>> f()
    5
    """
    return 5


class C:
    """
    Class docstring.

    >>> C().c(10)
    5
    """

    def c(self, n):
        """
        Method docstring.

        >>> c = C()  # counts as an example
        >>> c.c(10)  # not a duplicate; different AST
        5
        """
        return n // 2
