"""
This module lists many tests for the doctest-testing functionality,
including finding docstrings, finding doctests, requiring a certain
number of doctests, and requiring that doctests pass.

Note: This example is written slightly differently than the others: it
uses asserts to check return values from various optimism tests, whereas
normally you would not use such assertions, since optimism already
prints test results. The asserts here are to help make it easier to
debug this file during our own testing, but might make it harder to
debug things for an end user.
"""

import optimism

# No docstring
def a():
    pass

t = optimism.testFunction(a)
assert t.getDocstring() is None
assert t.checkHasDocstring() is False  # fails
assert t.checkDocTestCount(1) is False  # fails
assert t.checkDocTestsPass() is False  # fails (requires an example)

# Empty docstring
def b():
    ''
    pass

t = optimism.testFunction(b)
assert t.getDocstring() == ''
assert t.checkHasDocstring() is False  # fails, must be non-empty
assert t.checkDocTestCount(1) is False  # fails
assert t.checkDocTestsPass() is False  # fails (requires an example)

# Non-empty docstring without tests
def c():
    'hi'
    pass

t = optimism.testFunction(c)
assert t.getDocstring() == 'hi'
assert t.checkHasDocstring() is True  # passes
assert t.checkDocTestCount(1) is False  # fails
assert t.checkDocTestsPass() is False  # fails (requires an example)

# Single example
def d():
    """
    >>> d()
    3
    """
    return 3

t = optimism.testFunction(d)
dts = t.getDocTests()
assert len(dts) == 1
assert len(dts[0].examples) == 1
assert t.getDocstring() == '\n    >>> d()\n    3\n    '
assert t.checkHasDocstring() is True  # passes
assert t.checkDocTestsPass() is True  # passes
assert t.checkDocTestCount() is True  # passes
assert t.checkDocTestCount(1) is True  # passes
assert t.checkDocTestCount(2) is False  # fails (only one example)

# Single example (wrong)
def e():
    """
    >>> e()
    4
    """
    return 3

t = optimism.testFunction(e)
assert t.checkDocTestCount(1) is True
assert t.checkDocTestsPass() is False  # example is wrong

# Three correct examples
def f(x):
    """
    >>> f(1)
    2
    >>> f(2)
    3
    >>> f(3)
    4
    """
    return x + 1

t = optimism.testFunction(f)
assert t.checkDocTestCount() is True
assert t.checkDocTestCount(1) is True
assert t.checkDocTestCount(3) is True
assert t.checkDocTestCount(4) is False
assert t.checkDocTestsPass() is True

# Three correct examples w/ same source
G = 1
def g():
    """
    >>> g()
    2
    >>> g()
    3
    >>> g()
    4
    """
    global G
    G += 1
    return G

t = optimism.testFunction(g)
assert t.checkDocTestCount() is True
assert t.checkDocTestCount(3) is True
assert t.checkDocTestCount(4) is False
assert t.checkDocTestsPass() is True  # relies on them only being run once
assert G == 4  # does get changed as a side effect (TODO: counteract that?)
assert t.case().checkReturnValue(5) is True
assert t.case().checkReturnValue(6) is True
# expectations are wrong now that global value has changed.
assert t.checkDocTestsPass() is False
G = 1
assert t.checkDocTestsPass() is False  # now they pass again

# Two correct examples and one incorrect
def h(x):
    """
    >>> h(1)
    2
    >>> h(2)
    3
    >>> h(2)
    4
    """
    return x + 1

t = optimism.testFunction(h)
assert t.checkDocTestCount() is True
assert t.checkDocTestCount(3) is True
assert t.checkDocTestCount(4) is False
assert t.checkDocTestsPass() is False

# Three identical correct examples
def i(x):
    """
    >>> i(1)
    2
    >>> i(1)
    2
    >>> i(1)
    2
    """
    return x + 1

t = optimism.testFunction(i)
assert t.checkDocTestCount(1) is True
assert t.checkDocTestCount(2) is False  # examples are duplicates
assert t.checkDocTestsPass() is True

# Two correct examples and one incorrect, but first one is wrong
def j(x):
    """
    >>> j(1)
    3
    >>> j(2)
    3
    >>> j(3)
    4
    """
    return x + 1

optimism.freshTestSuite('countJ')
t = optimism.testFunction(j)
assert t.checkDocTestCount(3) is True
assert t.checkDocTestsPass() is False
trials = optimism.listTrialsInSuite()
assert len(trials) == 1
assert isinstance(trials[0], optimism.DocChecks)
assert trials[0].manager is t
outcomes = optimism.listOutcomesInSuite()
assert len(outcomes) == 4  # count check + 3 examples
assert outcomes[0][0] is True
assert outcomes[1][0] is False
assert outcomes[2][0] is True
assert outcomes[3][0] is True
optimism.testSuite('default')


# Tests w/ same expectations
def k(x):
    """
    >>> k(2)
    1
    >>> k(3)
    1
    """
    return x // 2

t = optimism.testFunction(k)
assert t.checkDocTestCount(2) is True
assert t.checkDocTestCount(3) is False
assert t.checkDocTestsPass() is True


# Generates an expected exception
def l(x):
    """
    >>> l(1)
    1.0
    >>> l(0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: ...
    >>> l(2)
    0.5
    """
    return 1 / x

t = optimism.testFunction(l)
assert t.checkDocTestCount(3) is True
assert t.checkDocTestCount(4) is False
assert t.checkDocTestsPass() is True


# Generates an unexpected exception
def m(x):
    """
    >>> m(1)
    2
    >>> m(2)
    3
    >>> m('1')
    '11'
    """
    return x + 1

t = optimism.testFunction(m)
assert t.checkDocTestCount(3) is True
assert t.checkDocTestCount(4) is False
assert t.checkDocTestsPass() is False


# Duplicates but fancy
def n(x):
    """
    >>> n(1)
    2
    >>> n(1) # comment
    2
    >>> n( 1   )
    2
    >>> n( 1   )
    ...
    2
    >>> n(
    ...   1
    ... )
    2
    """
    return x + 1

t = optimism.testFunction(n)
assert t.checkDocTestCount(1) is True
assert t.checkDocTestCount(2) is False  # duplicates
assert t.checkDocTestsPass() is True


# Counting examples is lexical, not based on actual calls
def o(x):
    """
    >>> for i in range(3):
    ...     print(o(i))
    1
    2
    3
    """
    return x + 1

t = optimism.testFunction(o)
assert t.checkDocTestCount(1) is True
assert t.checkDocTestCount(2) is False  # just counts prompts
assert t.checkDocTestsPass() is True

# Examples for include/exclude tests
def p(x):
    """
    >>> p(1)
    2
    >>> p(2)
    3
    >>> p(3)
    4
    >>> 5
    5
    """
    return x + 1

t = optimism.testFunction(p)
assert t.checkDocTestsPass() is True  # Doc tests do pass...

# Check counting with include and/or exclude
assert t.checkDocTestCount(4) is True
assert t.checkDocTestCount(5) is False
incl = [optimism.Call('p')]  # only 3 matching
assert t.checkDocTestCount(3, include=incl) is True
assert t.checkDocTestCount(4, include=incl) is False
incl = [optimism.Call('p'), optimism.Constant(1)]  # only 1 matching (AND)
assert t.checkDocTestCount(1, include=incl) is True
assert t.checkDocTestCount(2, include=incl) is False
excl = [optimism.Call('p')]  # only 1
assert t.checkDocTestCount(1, exclude=excl) is True
assert t.checkDocTestCount(2, exclude=excl) is False
excl = [optimism.Constant(1), optimism.Constant(2)]  # 2 left (OR)
assert t.checkDocTestCount(2, exclude=excl) is True
assert t.checkDocTestCount(3, exclude=excl) is False
# Strings as exact match filters
incl = ['p(2)']  # 1 match (specific)
assert t.checkDocTestCount(1, include=incl) is True
assert t.checkDocTestCount(2, include=incl) is False
excl = ['p(1)', 'p( 2 ) # comment']  # 2 matches left
assert t.checkDocTestCount(2, exclude=excl) is True
assert t.checkDocTestCount(3, exclude=excl) is False
# Function calls excluding specific examples
assert t.checkDocTestCount(1, include=incl, exclude=excl) is False
incl = [optimism.Call('p')]
assert t.checkDocTestCount(1, include=incl, exclude=excl) is True
assert t.checkDocTestCount(2, include=incl, exclude=excl) is False


# Test BlockManager docstrings
t = optimism.testBlock('''
"""
Block docstring w/ one example.
>>> 5
5
"""

def f():
    """
    Inner docstring.
    >>> f()
    5
    """
    print(5)

class C:
    """
    Class docstring.
    >>> C().c()
    5
    """
    def c(self):
        """
        Method docstring.
        >>> C().c()  # duplicate of example in class
        5
        """
        return 5
''')
assert t.getDocstring() == '\nBlock docstring w/ one example.\n>>> 5\n5\n'
assert t.checkHasDocstring() is True
assert t.checkDocTestCount(3) is True
assert t.checkDocTestCount(4) is False  # one duplicate
assert t.checkDocTestsPass() is True

# BlockManager without a docstring at top level
t = optimism.testBlock('def f():\n  "hi"\n  return 5')
assert t.getDocstring() is None
assert t.checkHasDocstring() is False
assert t.checkDocTestCount(1) is False
assert t.checkDocTestsPass() is False

# Same but has nested example
t = optimism.testBlock('def f():\n  """\n  >>> f()\n  5\n  """\n  return 5')
assert t.getDocstring() is None
assert t.checkHasDocstring() is False
assert t.checkDocTestCount(1) is True
assert t.checkDocTestCount(2) is False
assert t.checkDocTestsPass() is True

# Nested example is wrong
t = optimism.testBlock('def f():\n  """\n  >>> f()\n  4\n  """\n  return 5')
assert t.checkDocTestsPass() is False


# File manager
t = optimism.testFile('doc_example.py')
assert t.getDocstring() == '\nModule docstring.\n\n>>> 5\n5\n'
assert t.checkHasDocstring() is True
assert t.checkDocTestsPass() is True
assert t.checkDocTestCount(5) is True
assert t.checkDocTestCount(6) is False
assert t.checkDocTestCount(2, include=[optimism.Call('c')]) is True
assert t.checkDocTestCount(3, include=[optimism.Call('c')]) is False
# TODO: add a 'within' keyword for count checks (not easy)?
