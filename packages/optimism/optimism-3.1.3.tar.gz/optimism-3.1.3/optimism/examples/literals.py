"""
Examples for `getLiteralValue` and `Literal`.
"""

import optimism as opt

code = """
l = [1, 2, 3]
t = (4, 5, 6)
s = {7, 8, 8, 9}
d = {10: 11, 12: 13}
ls = ['list', 'of', 'strings']
structured = [{14: 15}, {16, 17}, (18, [19, 20, 21])]
"""

tester = opt.testBlock(code)
tester.checkCodeContains(opt.Literal([1, 2, 3]))
tester.checkCodeContains(opt.Literal((4, 5, 6)))
tester.checkCodeContains(opt.Literal({7, 8, 8, 9}))
tester.checkCodeContains(opt.Literal({7, 8, 9}))  # set elides duplicates
tester.checkCodeContains(opt.Literal({10: 11, 12: 13}))
tester.checkCodeContains(opt.Literal(['list', 'of', 'strings']))
tester.checkCodeContains(
    opt.Literal([{14: 15}, {16, 17}, (18, [19, 20, 21])])
)

tester.checkCodeContains(opt.Literal([4, 5, 6], types=tuple))
tester.checkCodeContains(opt.Literal([4, 5, 6], types=(list, tuple, set)))
tester.checkCodeContains(opt.Literal((7, 8, 8, 9), types=set))
tester.checkCodeContains(opt.Literal(types=list))
tester.checkCodeContains(opt.Literal(types=tuple))
tester.checkCodeContains(opt.Literal(types=set))
tester.checkCodeContains(opt.Literal(types=dict))
tester.checkCodeContains(opt.Literal(types=(list, dict)))

tester.checkCodeContains(opt.Literal([4, 5, 6]))  # fails
tester.checkCodeContains(opt.Literal((1, 2, 3)))  # fails

tester = opt.testBlock("'hi'")
tester.checkCodeContains(opt.Literal())  # fails
tester.checkCodeContains(opt.Literal(types=list))  # fails
tester.checkCodeContains(opt.Literal(types=tuple))  # fails
tester.checkCodeContains(opt.Literal(types=set))  # fails
tester.checkCodeContains(opt.Literal(types=dict))  # fails

tester = opt.testBlock("[4, 5, 6] + (4, 5, 6)")  # TypeError is irrelevant
tester.checkCodeContains(opt.Literal([4, 5, 6], n=1))
tester.checkCodeContains(opt.Literal((4, 5, 6), n=1))
tester.checkCodeContains(opt.Literal((4, 5, 6), types=(list, tuple), n=2))
tester.checkCodeContains(opt.Literal((4, 5, 6), types=(list, set), n=1))
tester.checkCodeContains(opt.Literal((4, 5, 6), types=(set, dict), n=0))

tester = opt.testBlock("[x, y, z]")
tester.checkCodeContains(opt.Literal(types=list))
