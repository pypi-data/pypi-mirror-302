"""
Basic demonstration of optimism code-structure checking functionality.
"""

import optimism

optimism.skipChecksAfterFail(None)


def askNameAge():
    "A function that uses input."
    name = input("What is your name? ")
    age = input("How old are you? ")
    return (name, age)


# Test manager for that function
tester = optimism.testFunction(askNameAge)

# A structural check to ensure that the above function uses `input`
tester.checkCodeContains(optimism.Call('input'))

# Checks with bounds on the number of use sites
tester.checkCodeContains(optimism.Call('input', min=2))
tester.checkCodeContains(optimism.Call('input', n=2))
tester.checkCodeContains(optimism.Call('input', max=2))

# A simple loop that uses print multiple times
for x in range(4):
    print(x)

# Some operators
if x < 3:
    print(x not in (1, 2, 3))


# Tester for this file
fileTester = optimism.testFile(__file__)

fileTester.checkCodeContains(optimism.Def())  # succeeds
fileTester.checkCodeContains(optimism.Def('askNameAge'))  # succeeds
fileTester.checkCodeContains(optimism.Def('functionName'))  # fails

fileTester.checkCodeContains(optimism.Def().contains(optimism.Return()))  # ✓
fileTester.checkCodeContains(optimism.Def().contains(optimism.Loop()))  # ✗
fileTester.checkCodeContains(optimism.Loop().contains(optimism.Def()))  # ✗
fileTester.checkCodeContains(optimism.Loop(only="while"))  # ✗
fileTester.checkCodeContains(optimism.Loop(only="for"))  # ✓

fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('print'))
)  # ✓
fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('range'))
)  # ✓
fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('print', n=1))
)  # ✓
fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('print', n=4))
)  # ✗
fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('print', min=4))
)  # ✗
fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('print', max=1))
)  # ✓
fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('print', max=0))
)  # ✗
fileTester.checkCodeContains(
    optimism.Loop().contains(optimism.Call('notCalled', min=0))
)  # ✓

fileTester.checkCodeContains(
    optimism.IfElse().contains(optimism.Operator('<'))
)  # ✓
fileTester.checkCodeContains(
    optimism.IfElse().contains(optimism.Operator('>'))
)  # ✗
fileTester.checkCodeContains(
    optimism.IfElse().contains(optimism.Operator('in'))
)  # ✓
fileTester.checkCodeContains(
    optimism.IfElse().contains(optimism.Operator('not in'))
)  # ✓

# Testing constant matching w/ types/values
('a', 2, 5.0)
fileTester.checkCodeContains(optimism.Constant('a'))  # ✓
fileTester.checkCodeContains(optimism.Constant(2))  # ✓
fileTester.checkCodeContains(optimism.Constant(4.0 / 2))  # ✓
fileTester.checkCodeContains(optimism.Constant(4.0 / 2, float))  # ✗
fileTester.checkCodeContains(optimism.Constant(4.0 / 2, int))  # ✓
fileTester.checkCodeContains(optimism.Constant(5.0, int))  # ✗
fileTester.checkCodeContains(optimism.Constant(5.0, float))  # ✓
