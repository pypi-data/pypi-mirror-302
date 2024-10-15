from optimism import *

# Simple example function
def f(x, y):
    "Example function"
    return x + y + 1

# Simple test for that function
test = testFunction(f) # line 9
case = test.case(1, 2)
case.checkReturnValue(3) # line 11


# Function that prints multiple lines of output
def display(message):
    print("The message is:")
    print('-' + message + '-')


# One test case with two lines of output
test = testFunction(display) # line 20
case = test.case('hello')
case.checkPrintedLines('The message is:', '-hello-') # line 22


# A function that uses input
def askNameAge():
    name = input("What is your name? ")
    age = input("How old are you? ")
    return (name, age)


test = testFunction(askNameAge) # line 31
case = test.case()
case.provideInputs("Name", "thirty")
case.checkReturnValue(('Name', 'thirty')) # line 34
case.checkPrintedLines(
    'What is your name? Name',
    'How old are you? thirty' # line 37
)
