"""
Examples of test suite functionality.
"""

import optimism

def f(x, y):
    print(x)
    return x * y

optimism.testSuite('A')

tester = optimism.testFunction(f)
tester.checkCodeContains(optimism.Call('print'))
c = tester.case(2, 3)
c.checkPrintedLines('2')
c.checkReturnValue(6)

z = f(3, 4)
optimism.expect(z, 12)

optimism.testSuite('B')

tester.checkCodeContains(optimism.Return())
c = tester.case(4, 5)
c.checkPrintedLines('5')
c.checkReturnValue(20)

optimism.expectType(f('a', 4), str)

optimism.showSummary()
optimism.showSummary('A')

optimism.testSuite('C')

print("Outcomes in suite A:")
for outcome in optimism.listOutcomesInSuite('A'):
    print(outcome)

print("Outcomes in suite B:")
for outcome in optimism.listOutcomesInSuite('B'):
    print(outcome)

optimism.testSuite('A')

optimism.expect(3 + 4, 7)

optimism.testSuite('C')

print("Outcomes in suite A (again):")
for outcome in optimism.listOutcomesInSuite('A'):
    print(outcome)

optimism.resetTestSuite('A')

print("No more outcomes in suite A:", optimism.listOutcomesInSuite('A'))

optimism.freshTestSuite('B')

print("No more outcomes in suite B:", optimism.listOutcomesInSuite('B'))

optimism.deleteAllTestSuites()

try:
    optimism.listOutcomesInSuite('B')
except ValueError:
    print("No more suite B.")
