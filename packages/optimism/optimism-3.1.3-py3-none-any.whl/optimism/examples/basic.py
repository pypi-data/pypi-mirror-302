"""
Basic demonstration of optimism core testing functionality.
"""

import optimism


# Simple example function
def f(x, y):
    "Example function"
    return x + y + 1


# Simple test for that function
t = optimism.testFunction(f)
t.case(1, 2).checkReturnValue(4)  # line 16


# Function that prints multiple lines of output
def display(message):
    print("The message is:")
    print('-' + message + '-')


# Multi-line output test
t = optimism.testFunction(display)
t.case('hello').checkPrintedLines('The message is:', '-hello-')  # line 27


def askNameAge():
    "A function that uses input."
    name = input("What is your name? ")
    age = input("How old are you? ")
    return (name, age)


# One test case with specific inputs that checks both the return value
# and what is printed
test = optimism.testFunction(askNameAge)  # line 39
case = test.case()
case.provideInputs("Name", "thirty")
case.checkReturnValue(('Name', 'thirty'))  # line 42
case.checkPrintedLines(  # line 43
    'What is your name? Name',
    'How old are you? thirty'  # line 45
)

optimism.showSummary()

# These checks will show details about the expressions used (like the
# value of x):
x = 3
y = 4
optimism.testFunction(f).case(x + x, y).checkReturnValue(10)  # fails (is 11)
optimism.expect(f(x + x, y), 10)  # fails; shows x

# Increase detail level
optimism.detailLevel(1)

c = optimism.testFunction(display).case('nope')
c.checkReturnValue(False)  # fails (result is None)
c.checkPrintedLines('The message is:', '-nope-')  # succeeds

optimism.detailLevel(0)
c.checkPrintedLines('The message is:', '-yep-')  # fails

# For loop test
for x in range(3):
    t = optimism.testFunction(f).case(x, x).checkReturnValue(5)
    # fails except when x == 2

optimism.showSummary()
