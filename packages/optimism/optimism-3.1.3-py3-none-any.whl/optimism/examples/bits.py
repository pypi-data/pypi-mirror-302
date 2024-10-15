import optimism as opt

x = [1, 2, 3]
y = [4, 5, 6]
x.append(y)

opt.detailLevel(1)

opt.expect(x, [1, 2, 3, [4, 5, 6]])

y.pop()
opt.expect(x, [1, 2, 3, [4, 5]])
opt.expect(x[3], y)
opt.expect(x[3][-1], 5)

x.pop()
opt.expect(x, [1, 2, 3])
opt.expect(x[1], 2)

opt.expect(x, [1, 2, 3])
x.pop()
opt.expect(x, [1, 2])

# This... doesn't work
opt.expect(x[-1], x.pop())

opt.expectType(x, list)
opt.expectType(x[0], int)
