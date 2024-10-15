import optimism as opt


def interactive():
    """
    An interactive function for testing purposes.
    """
    x = input('Y?')
    print(x + ' Z!')
    return x


# Call it once before testing
interactive()

m = opt.testFunction(interactive)
c = m.case()
c.provideInputs('Q')
c.checkPrintedLines('Y?Q', 'Q Z!')
c.checkReturnValue('Q')

c = m.case()
c.provideInputs('A')
c.checkPrintedLines('Y?A', 'A Z!')
c.checkReturnValue('A')

c = m.case()
c.provideInputs('A')
c.provideInputs('B') # this is okay, and redefines the inputs
c.checkPrintedLines('Y?B', 'B Z!')
c.checkReturnValue('B')


# This isn't allowed
try:
    c.provideInputs('N')
except opt.TestError:
    print("Re-providing input was blocked.")

# Does input/output capturing mess with this?
print("Hello")

# Call it again after releasing input & output
interactive()
