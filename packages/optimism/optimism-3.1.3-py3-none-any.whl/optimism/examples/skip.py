import optimism as opt

t = opt.testFunctionMaybe(opt, 'indent')
t.case('hi', 2).checkReturnValue('  hi')

t2 = opt.testFunctionMaybe(opt, 'indetn')
t2.case('hi', 2).checkReturnValue('  hi')
t2.case('hi', 2).checkPrintedLines('')


def f():
    return 3


opt.skipChecksAfterFail("case")

t3 = opt.testFunction(f)
c1 = t3.case()
c1.checkReturnValue(4)
c1.checkReturnValue(5) # will be skipped
c1.checkReturnValue(3) # will be skipped

c2 = t3.case()
c2.checkReturnValue(3) # won't be skipped

opt.skipChecksAfterFail("manager")

t3 = opt.testFunction(f)
t3.case().checkReturnValue(4)
t3.case().checkReturnValue(5) # will be skipped
t3.case().checkReturnValue(3) # will be skipped

opt.skipChecksAfterFail(None)

t3 = opt.testFunction(f)
t3.case().checkReturnValue(4)
t3.case().checkReturnValue(5) # will NOT be skipped
t3.case().checkReturnValue(3) # will NOT be skipped
