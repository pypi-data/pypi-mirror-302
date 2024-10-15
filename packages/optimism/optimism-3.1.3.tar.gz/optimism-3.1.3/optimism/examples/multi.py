import optimism as opt

opt.detailLevel(1)
for i in range(3):
    # Note: long line is intentional to test handling multiple testCase
    # calls on one line of code...
    [opt.expect(i, i), opt.expect(i + 1, i + 1), opt.expect(i * i, i * i)]

opt.expect(
    (
        1,
        2,
        3
    ),
    (1, 2, 3)
)
