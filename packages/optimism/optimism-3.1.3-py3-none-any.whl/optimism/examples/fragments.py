"""
Examples for `checkPrintedFragment`
"""

import optimism as opt


def f():
    """
    Prints a few lines of output for testing...
    """
    print("ABC")
    print("DEF ")
    print("GHI")


m = opt.testFunction(f)
c = m.case()
c.checkPrintedFragment('AB')
c.checkPrintedFragment('C\nD')
c.checkPrintedFragment('ABC\nDEF\nGHI')
c.checkPrintedFragment('\n', 3, False)
c.checkPrintedFragment('\n', 2, True)
