import optimism as opt

name = opt.trace(input("What is your name? "))
greeting = opt.trace("Hello " + opt.trace(name))
underline = opt.trace('=' * len(greeting))
opt.trace(print(greeting))
print(opt.trace(underline))

opt.trace("ha" * 50)

opt.detailLevel(1)
opt.trace("ha" * 50)
