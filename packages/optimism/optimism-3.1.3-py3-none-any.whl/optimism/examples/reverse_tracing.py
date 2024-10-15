"""
An example file for reverse tracing, i.e., state validation. Comments
starting with '##', '#:', '#>', '#.', and '#N' where N is an integer
have special meanings (see below).
"""

import optimism

# Comments started with '##', '#:', and '#>' are special.
# A comment starting with '##' specifies program state changed since the
# previous such comment. Multiple lines of '##' are grouped together and
# checked after the first program line above them; multiple state
# changes can be separated by commas and/or spaces.

x = 5
## x=5
y = x + 3
## y=8
print(x, '\\n', y)
## prints:
## '5 '
## ' 8'

x, y = y, x

## x=8
## y=5

x = y
y = x
print(x, y)
## x=5, y=5, prints: "5 5"

# A comment starting with '#:' defines a code block which can have
# multiple specified state evolutions. Note that 'input:' specifications
# have to happen before the line where input occurs, although when
# multiple values are specified, they can apply to multiple future
# inputs.

#:
## input: 'Peter'
name = input("What is your name? ")
## prints: 'What is your name? Peter'
## input: 'Pink'
fav = input("What is your favorite color? ")
## prints: 'What is your favorite color? Pink'
print("Hello", name)
print("I like", fav, "too!")
## prints: 'Hello Peter' 'I like Pink too!'

# A '#>' comment specifies a secondary state sequence for the first '#:'
# block above it. The state changes listed have to happen in the order
# they appear, but no specific lines are targeted. When checking a file,
# first the entire file is checked using any checks which appear
# outside of code blocks, and ignoring checks in functions and classes
# entirely (but that code will still run if called). Then any code block
# specifications including specifications in functions are checked
# against just the code they apply to, without re-running the whole file.

#>
## input: 'Nobody'
## prints: 'What is your name? Nobody'
## input: 'black'
## prints:
## 'What is your favorite color? black'
## 'Hello Nobody'
## 'I like black too!'

# Multiple '#>' can occur following a single '#:'. 'input:'
# specifications are not state changes, so they don't have to be
# specified in order relative to state changes for a '#>' block to
# succeed.

#> input: 'Helia' 'yellow'
## prints: 'What is your name? Helia' 'What is your favorite color? yellow'
## 'Hello Helia' 'I like yellow too!'

# Not every line of code needs to have a state change specified, although
# you may want to require this to ensure students understand everything
# they wrote. Some lines (like 'pass') don't change state.

GLOBAL = 5

pass

# Code in a code block gets executed line-by-line, independently of other
# code in the file. Any function parameters or global variables used must
# be specified on the '#:' line.


def f(x, y):
    "Docstring here"
    #: x=3, y=4, GLOBAL=3
    x += GLOBAL
    ## x = 6
    result = x + y
    ## result=10
    print(result)
    ## prints:
    ## '10'
    return result // 2
    ## returns 5

# A code block ends at the end of a function or class definition, or
# wherever the next '#>' starts. So this line is not part of the code
# block above, and will only be checked on the initial run of the file,
# where it will get a value for 'GLOBAL' from the definition before the
# function.


GLOBAL += 2
## GLOBAL = 7

# This replay applies to the first '#:' block above it, which is in the
# function f.

#> x=1, y=2, GLOBAL=4
## x=5, result=7, prints: '7', returns 3

# If a 'state change' is specified which is not a change from previous
# state, that's OK (as long as it does match the program state that
# exists where it is specified). Note that state assignments made for
# replays and/or code blocks don't affect the values of variables during
# the initial check of the file, nor do they affect the values of
# variables during checks of other code blocks.

## GLOBAL = 7

# You can use '#.' to end a code block early.

#: GLOBAL = 23
GLOBAL += 7
## GLOBAL = 30
print(GLOBAL)
## prints: '30'
#.

# The code below ignores the initial value and check in the code block
# above, but is affected by the code in the code block because that's
# code that would run during the execution of the file.

GLOBAL += 1
## GLOBAL = 15

# This replay applies to the previous code block, which does not include
# the line and check just above this comment, because of the '#.' which
# ended the code block without including them. Note that '= 3' and '= 10'
# have different meanings (assignment vs. check) because the first
# appears on a '#>' line and the second does not.

#> GLOBAL = 3
## GLOBAL = 10
## prints: '10'

# Multiple '#>' in a row can be used if you need to make more initial
# assignments than will fit on one line.
#> GLOBAL =
#> 5
## GLOBAL = 12 prints: '12'

# To specify a multi-line string in a check, use triple quotes or '\\n'.
# With triple-quotes, a single space after '##' will be stripped from
# each continuing line.

#:
message = '''This is a multi-
line string!
'''
## message = "This is a multi-\\nline string!\\n"

#>
## message = '''This is a multi-
## line string!
## '''

# When iteration or other repetition happens, use semicolons to indicate
# successive state changes that apply to multiple visits to that line.
# Checks will be split by ';' first, then ',' (or just spaces). You may
# also use '#' followed by an integer (starting from 0) to indicate which
# check applies to which iteration.

x = 4
y = 0
#:
## x = 4, y = 0
for i in range(3):
    ## i = 0; i = 1; i = 2
    x += i
    ## x = 4;
    ## x = 1;
    ## x = 6
    x, y = y, x
    ## x = 0, y = 4
    ##; x = 4, y = 1
    ##; x = 1, y = 6
    print(x, y)
    #0 prints: '0 4'
    #1 prints: '4 1'
    #2 prints: '1 6'

# Note that in a replay, you must specify the #0/#1/#2 etc. successively,
# you cannot say '#0 #0 #0 ... #1 #1 #1' (but see below).

#> x = 3, y = 3
## x = 3, y = 3
#0 i = 0
#1 i = 1
#2 i = 2
#0 x = 3
#1 x = 4
#2 x = 5
#0 x = 3, y = 3
#1 x = 3, y = 4
#2 x = 4, y = 5
#0 prints: '3 3'
#1 prints: '3 4'
#2 prints: '4 5'

# In a replay, it's perfectly acceptable to unroll the loop, although
# this is not possible syntactically in the initial code block notation.
# Replays cannot specify the timing of state changes as precisely as
# initial code blocks can, because their state changes aren't associated
# with particular lines of code.

#> x = 3, y = 3
## x = 3, y = 3
## i = 0
## x = 3
## x = 3, y = 3
## prints: '3 3'
## i = 1
## x = 4
## x = 3, y = 4
## prints: '3 4'
## i = 2
## x = 5
## x = 4, y = 5
## prints: '4 5'

# The ';' syntax and '#0', '#1' syntax can be combined, which is useful
# for nested loops; the passes specified using ';' are grouped together
# into phases specified by '#0', '#1', etc. The special syntax '#*' can
# be used to indicate a series of states (separated by ';') which cycle
# indefinitely.

# Also note that when you need to line wrap a numbered state line,
# continue using '##' rather than the integer.

#:
result = ''
## result = ''
for i in range(3):
    ## i = 0; i = 1; i = 2
    for j in range(3):
        #* j = 0; j = 1; j = 2
        s = '0' * i + '1' * j
        #0 s = ''; s = '1'; s = '11'
        #1 s = '0'; s = '01'; s = '011'
        #2 s = '00'; s = '001'; s = '0011'
        result += s + '\\n'
        #0 result = '\\n'; result = '\\n1\\n'; result='\\n1\\n11\\n'
        #1 result = '\\n1\\n11\\n0\\n';
        ##   result = '\\n1\\n11\\n0\\n01\\n';
        ##   result = '\\n1\\n11\\n0\\n01\\n011\\n';
        #2 result = '\\n1\\n11\\n0\\n01\\n011\\n00\\n';
        ##   result = '\\n1\\n11\\n0\\n01\\n011\\n00\\n001\\n';
        ##   result = '\\n1\\n11\\n0\\n01\\n011\\n00\\n001\\n0011\\n';

# State values may be specified using Python primitives: tuples, lists,
# sets, and dictionaries, plus integers, floats, complexes, strings,
# byte-strings, booleans, and None. The use of variables or function
# calls is not allowed. For specifying state of a custom object, the
# left-hand side of a state specifier may be a dotted attribute. Partial
# state may also be specified using indices, and indices and attributes
# may be combined. += may also be used to specify a state update, this
# will be used relative to the previous state specification.

x = [1, 2, {3: 4, 5: 'six'}]
## x = [1, 2, {3: 4, 5: 'six'}]
x[0] += 1
## x[0] += 1
x[2][5] = 'sixteen'
## x[2][5] += 'teen'


class P:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'


p = P(1, 2)
## p.x = 1, p.y = 2
p.x = 5
## p.x = 5
print(p)
## prints: '(5, 2)'

manager = optimism.testFile('reverse_tracing.py')
manager.validateStates()
