import optimism as opt

# Don't skip checks after one fails
opt.skipChecksAfterFail(None)

m = opt.testFile("io_example.py")
c = m.case()
c.provideInputs("Tester")
c.checkPrintedLines(
    'What is your name? Tester',
    'Hi Tester!',
    '==========',
)


def sameLengthLines(testResults):
    """
    Checks that the second and third lines of the output are the same
    length as each other.
    """
    lines = testResults["output"].splitlines()
    if len(lines) < 3:
        return "Fewer than 3 lines of output."
    l1 = len(lines[1])
    l2 = len(lines[2])
    if l1 != l2:
        return (
            f"Second and third lines have different lengths ({l1} and"
            f" {l2})."
        )
    else:
        return True


c.checkCustom(sameLengthLines)


def customFail(_):
    return "failure message"


c.checkCustom(customFail)


def checkSecondLine(testResults, checkAgainst):
    """
    Checks that the second line of the output is equal to a specific
    string.
    """
    lines = testResults["output"].splitlines()
    if lines[1] == checkAgainst:
        return True
    else:
        return f"'{lines[1]}' did not match '{checkAgainst}'"


c.checkCustom(checkSecondLine, 'Hi Tester!')
c.checkCustom(checkSecondLine, 'Hi Tester?')
