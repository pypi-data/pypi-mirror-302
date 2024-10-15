import optimism as opt

x = 3

m = opt.testBlock(
    """\
print(x)
x += 1
print(x)"""
)
c = m.case()
c.checkPrintedLines('3', '4')
c.checkVariableValue('x', 5)
c = m.case(x=5)
c.checkPrintedLines('5', '6')
c.checkVariableValue('x', 6)


m = opt.testBlock(
    """\
x = 3
print(x)
x += 1
print(x)
x += 1"""
)
c = m.case()
c.checkPrintedLines('3', '4')
c.checkVariableValue('x', 5)
c.checkVariableValue('x', 6)
