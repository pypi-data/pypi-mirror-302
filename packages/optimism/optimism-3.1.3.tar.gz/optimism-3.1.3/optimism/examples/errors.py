import optimism as opt

import bad

t = opt.testFunction(bad.f)
t.case().checkReturnValue(None)
