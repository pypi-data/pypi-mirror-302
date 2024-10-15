"""
Examples for `checkVariableStructure` and `checkReturnedStructure`.

TODO: Include these results in tox...
"""

import optimism as opt


def f():
    result = [1, 2]
    result.append([3, 4])
    result.append(result)
    return result


tester = opt.testFunction(f)
tester.case().checkReturnedStructure('''\
@0: [1, 2, @1, @0]
@1: [3, 4]
''')
tester.case().checkReturnedStructure('''\
@0: [1, 2, @1, @0]
@1: [3, 4]
@2: ['extra']
''')  # should fail
tester.case().checkReturnedStructure(f())

tester = opt.testBlock('''\
x = 5
y = 10
''')
tester.case().checkVariableStructure('x', 5)
tester.case().checkVariableStructure('y', 10)
tester.case(z=6).checkVariableStructure('z', 6)


tester = opt.testBlock('''\
x = []
x.append([])
x.append(set())
x[0].append(x)
x[1].add((1, 2))
''')

twisted = []
twisted.append([])
twisted.append(set())
twisted[0].append(twisted)
twisted[1].add((1, 2))

tester.case().checkVariableStructure('x', twisted)


tester = opt.testBlock('''\
x = [[1, 2], [1, 2]]
y = [[1, 2]]
y.append(y[0])
''')

tester.case().checkVariableStructure('x', '''\
x: @0
@0: [@1, @2]
@1: [1, 2]
@2: [1, 2]
''')
tester.case().checkVariableStructure('y', '''\
y: @5
@5: [@10, @10]
@10: [1, 2]
''')

tester = opt.testBlock('x = [[1, 2]]')
tester.case().checkVariableStructure('x', 'x: @0\n@0: [@1]\n@1: [1, 2]')
tester.case().checkVariableStructure('x', 'x: @0\n@0: [@1]\n@1: [1]')
tester.case().checkVariableStructure('x', 'x: @0\n@0: [@1]\n@1: [1, 2, 3]')
tester.case().checkVariableStructure('x', 'x: @0\n@0: [@1]\n@1: [3, 4]')

tester = opt.testBlock('x = ((1, 2),)')
tester.case().checkVariableStructure('x', 'x: @0\n@0: (@1,)\n@1: (1, 2)')
tester.case().checkVariableStructure('x', 'x: @0\n@0: (@1,)\n@1: (1,)')
tester.case().checkVariableStructure('x', 'x: @0\n@0: (@1,)\n@1: (1, 2, 3)')
tester.case().checkVariableStructure('x', 'x: @0\n@0: (@1,)\n@1: (3, 4)')

tester = opt.testBlock('''\
x = ((1, 2),)
x = x + (x[0],)
y = x[0]
y = y + (3,)
''')
tester.case().checkVariableStructure('x', '''\
x: @0
@0: (@1, @1)
@1: (1, 2)
''')
tester.case().checkVariableStructure('x', '''\
x: @7
@7: (@3, @3)
@3: (1, 2)
''')
tester.case().checkVariableStructure('y', '''\
y: @0
@0: (1, 2, 3)
''')
tester.case().checkVariableStructure('x', '''\
x: @0
@0: (@1, @1)
@1: (1, 2, 3)
''')  # should fail
tester.case().checkVariableStructure('x', '''\
x: @0
@0: (@3, @3)
@3: (1, 2, 3)
''')  # should fail
