import optimism as opt

words = ['hi', 'bye']
pair = [words, words]
print(opt.memoryReport(words=words, pair=pair))

knot = [pair, words]
knot.append(knot)
print(opt.memoryReport(pair=pair, words=words, knot=knot))

code = """\
a = []
b = []
b.append([])
a.append(b)
a.append([])
import math  # don't allow deep copy of env for this code
"""

tester = opt.testBlock(code)
case = tester.case()
case.checkVariableStructure('a', [[[]], []])
case.checkCustom(
    lambda result: result['scope']['a'][0] is result['scope']['b']
)
