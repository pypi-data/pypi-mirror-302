import optimism


def write123(filename):
    with open(filename, 'w') as fout:
        fout.write('1\n2\n3\n')


tester = optimism.testFunction(write123)
tester.case('a.txt').checkFileLines("a.txt", '1', '2', '3')
tester.case('b.txt').checkFileLines("b.txt", '1', '2', '3')
tester.case('b.txt').checkFileLines("b.txt", '1', '2')
tester.case('b.txt').checkFileLines("b.txt", '1', '2', 'hello')


def writeReturny(filename):
    with open(filename, 'w') as fout:
        fout.write('abc\r\r\n')
        fout.write('def\r\r\n')


tester = optimism.testFunction(writeReturny)
tester.case('a.txt').checkFileLines('a.txt', 'abc', 'def')
optimism.attendTrailingWhitespace()
tester.case('a.txt').checkFileLines('a.txt', 'abc', 'def')
# This check should fail
optimism.attendTrailingWhitespace(False) # set back to default


def writeNoNL(filename):
    with open(filename, 'w') as fout:
        fout.write('abc\n')
        fout.write('def')


tester = optimism.testFunction(writeNoNL)
tester.case('a.txt').checkFileLines('a.txt', 'abc', 'def')
optimism.attendTrailingWhitespace()
tester.case('a.txt').checkFileLines('a.txt', 'abc', 'def')
# This check should still pass, since even with
# IGNORE_TRAILING_WHITESPACE off, final newline from lines should be
# adjusted to match observed output.
optimism.attendTrailingWhitespace(False) # set back to default


optimism.expect('abc\ndef', 'abc\ndef\n')
optimism.attendTrailingWhitespace()
optimism.expect('abc\ndef', 'abc\ndef\n')
# This check should fail
optimism.attendTrailingWhitespace(False)
