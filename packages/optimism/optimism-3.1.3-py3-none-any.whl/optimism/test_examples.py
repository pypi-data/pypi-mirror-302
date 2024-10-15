import os
import sys
import io
import importlib
import re

from . import optimism

optimism.skipChecksAfterFail(None)
optimism.suppressErrorDetailsAfterFail(None)

# Detect whether we've got better or worse line numbers so we can create
# correct tests...
better_line_numbers = sys.version_info >= (3, 8)

EXAMPLES = [
    ("basic", []),
    ("bits", []),
    ("multi", []),
    ("block", []),
    ("runfile", ["Tester"]),
    ("tracing", ["Tester"]),
    ("catch_and_release", ["one", "two"]),
    ("skip", []),
    ("fragments", []),
    ("errors", []),
    ("files", []),
    ("code", []),
    ("suites", []),
    ("literals", []),
    ("structure", []),
    ("doctests", []),
    ("memoryReports", [])
    #("reverse_tracing", []),
    # TODO: Include this once the machinery for it is there
]


EXPECTATIONS = {
    "basic": [
        "✓ {file}:16",
        "✓ {file}:27",
        "✓ {file}:42",
        "✓ {file}:43" if better_line_numbers else "✓ {file}:45",
        """\
-- Summary for suite 'default' --
All 4 expectation(s) were met.
----
""",
        """\
✗ {file}:54
  Result:
    11
  was NOT equivalent to the expected value:
    10
  Called function 'f' with arguments:
    x = 6
    y = 4""",
        """\
✗ {file}:55
  Result:
    11
  was NOT equivalent to the expected value:
    10
  Test expression was:
    f(x + x, y)
  Values were:
    x = 3
    y = 4""",
        """\
✗ expectation from {file}:61 NOT met for test case at {file}:60
  Result:
    None
  was NOT equivalent to the expected value:
    False
  Called function 'display' with arguments:
    message = 'nope'""",
        """\
✓ expectation from {file}:62 met for test case at {file}:60
  Printed lines:
    \"\"\"\\
    The message is:
    -nope-
    \"\"\"
  were exactly the same as the expected printed lines:
    \"\"\"\\
    The message is:
    -nope-
    \"\"\"
  Called function 'display' with arguments:
    message = 'nope'""",
        """\
✗ {file}:65
  Printed lines:
    \"\"\"\\
    The message is:
    -nope-
    \"\"\"
  were NOT the same as the expected printed lines:
    \"\"\"\\
    The message is:
    -yep-
    \"\"\"
  First difference was:
    strings differ on line 2 where we got:
      '-nope-'
    but we expected:
      '-yep-'
  Called function 'display' with arguments:
    message = 'nope'""",
        """\
✗ {file}:69
  Result:
    1
  was NOT equivalent to the expected value:
    5
  Called function 'f' with arguments:
    x = 0
    y = 0""",
        """\
✗ {file}:69
  Result:
    3
  was NOT equivalent to the expected value:
    5
  Called function 'f' with arguments:
    x = 1
    y = 1""",
        "✓ {file}:69",
        """\
-- Summary for suite 'default' --
6 of the 12 expectation(s) were NOT met:
  ✗ {file}:54
  ✗ {file}:55
  ✗ {file}:61
  ✗ {file}:65
  ✗ {file}:69
  ✗ {file}:69
----"""
    ],

    "bits": [
        """\
✓ {file}:9
  Result:
    [1, 2, 3, [4, 5, 6]]
  was equivalent to the expected value:
    [1, 2, 3, [4, 5, 6]]
  Test expression was:
    x
  Values were:
    x = [1, 2, 3, [4, 5, 6]]""",
        """\
✓ {file}:12
  Result:
    [1, 2, 3, [4, 5]]
  was equivalent to the expected value:
    [1, 2, 3, [4, 5]]
  Test expression was:
    x
  Values were:
    x = [1, 2, 3, [4, 5]]""",
        """\
✓ {file}:13
  Result:
    [4, 5]
  was equivalent to the expected value:
    [4, 5]
  Test expression was:
    x[3]
  Values were:
    x = [1, 2, 3, [4, 5]]
    x[3] = [4, 5]""",
        """\
✓ {file}:14
  Result:
    5
  was equivalent to the expected value:
    5
  Test expression was:
    x[3][-1]
  Values were:
    x = [1, 2, 3, [4, 5]]
    x[3] = [4, 5]
    x[3][-1] = 5""",
        """\
✓ {file}:17
  Result:
    [1, 2, 3]
  was equivalent to the expected value:
    [1, 2, 3]
  Test expression was:
    x
  Values were:
    x = [1, 2, 3]""",
        """\
✓ {file}:18
  Result:
    2
  was equivalent to the expected value:
    2
  Test expression was:
    x[1]
  Values were:
    x = [1, 2, 3]
    x[1] = 2""",
        """\
✓ {file}:20
  Result:
    [1, 2, 3]
  was equivalent to the expected value:
    [1, 2, 3]
  Test expression was:
    x
  Values were:
    x = [1, 2, 3]""",
        """\
✓ {file}:22
  Result:
    [1, 2]
  was equivalent to the expected value:
    [1, 2]
  Test expression was:
    x
  Values were:
    x = [1, 2]""",
        """\
✓ {file}:25
  Result:
    2
  was equivalent to the expected value:
    2
  Test expression was:
    x[-1]
  Values were:
    x = [1]
    x[-1] = 1""",
        """\
✓ {file}:27
  The result type (<class 'list'>) was the expected type.
  Test expression was:
    x
  Values were:
    x = [1]""",
        """\
✓ {file}:28
  The result type (<class 'int'>) was the expected type.
  Test expression was:
    x[0]
  Values were:
    x = [1]
    x[0] = 1""",
    ],

    "block": [
        """\
✗ {file}:12
  Failed due to an error:
    Traceback omitted
    NameError: name 'x' is not defined
  Ran code:
    print(x)
    x += 1
    print(x)""",
        """\
✗ {file}:13
  Failed due to an error:
    Traceback omitted
    NameError: name 'x' is not defined
  Ran code:
    print(x)
    x += 1
    print(x)""",
        "✓ {file}:15",
        "✓ {file}:16",
        "✓ {file}:28",
        "✓ {file}:29",
        """\
✗ {file}:30
  Variable 'x' with value:
    5
  was NOT equivalent to the expected value:
    6
  Ran code:
    x = 3
    print(x)
    x += 1
    print(x)
    x += 1""",
    ],

    "multi": [
        f"""\
✓ {{file}}:7
  Result:
    {eval(expr)}
  was equivalent to the expected value:
    {eval(expr)}
  Test expression was:
    {expr}
  Values were:
    i = {i}"""
        for i in range(3)
        for expr in ["i", "i + 1", "i * i"]
    ] + [
         """\
✓ {file}:9
  Result:
    (1, 2, 3)
  was equivalent to the expected value:
    (1, 2, 3)
  Test expression was:
    (
            1,
            2,
            3
        )""" if better_line_numbers else """\
✓ {file}:15
  Result:
    (1, 2, 3)
  was equivalent to the expected value:
    (1, 2, 3)
  Test expression was:
    (
        1,
        2,
        3
    )""",
    ],

    "runfile": [
        "✓ {file}:9" if better_line_numbers else "✓ {file}:12",
        "✓ {file}:35",
        """\
✗ {file}:42
  Custom check failed:
    failure message
  Ran file 'io_example.py'""",
        "✓ {file}:57",
        """\
✗ {file}:58
  Custom check failed:
    'Hi Tester!' did not match 'Hi Tester?'
  Ran file 'io_example.py'""",
    ],

    "tracing": [
        "3 input(\"What is your name? \") ⇒ 'Tester'",
        "4 name ⇒ 'Tester'",
        "4 \"Hello \" + opt.trace(name) ⇒ 'Hello Tester'",
        "5 '=' * len(greeting) ⇒ '============'",
        "6 print(greeting) ⇒ None",
        "7 underline ⇒ '============'",
        "9 \"ha\" * 50 ⇒ 'hahahahahahahahahahahahahahahahahaha...",
        """\
{file}:12 "ha" * 50 ⇒ 'hahahahahahahahahahahahahahahahahaha...
  Full result is:
    'hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha'""", # noqa
    ],

    "catch_and_release": [
        "✓ {file}:19",
        "✓ {file}:20",
        "✓ {file}:24",
        "✓ {file}:25",
        "✓ {file}:30",
        "✓ {file}:31",
    ],

    "skip": [
        "✓ {file}:4",  # appears twice
        "Did not find 'indetn' in module 'optimism'...",
        "~ {file}:7 (skipped)",
        "~ {file}:8 (skipped)",
        """\
✗ {file}:19
  Result:
    3
  was NOT equivalent to the expected value:
    4
  Called function 'f'""",
        "~ {file}:20 (skipped)",
        "~ {file}:21 (skipped)",
        "✓ {file}:24",
        """\
✗ {file}:29
  Result:
    3
  was NOT equivalent to the expected value:
    4
  Called function 'f'""",
        "~ {file}:30 (skipped)",
        "~ {file}:31 (skipped)",
        """\
✗ {file}:36
  Result:
    3
  was NOT equivalent to the expected value:
    4
  Called function 'f'""",
        """\
✗ {file}:37
  Result:
    3
  was NOT equivalent to the expected value:
    5
  Called function 'f'""",
        "✓ {file}:38",
    ],

    "fragments": [
        "✓ {file}:19",
        "✓ {file}:20",
        "✓ {file}:21",
        "✓ {file}:22",
        "✓ {file}:23",
    ],

    "errors": [
        """\
✗ {file}:6
  Failed due to an error:
    Traceback omitted
    ZeroDivisionError: division by zero
  Called function 'f'"""
    ],

    "files": [
        "✓ {file}:10",
        "✓ {file}:11",
        '''\
✗ {file}:12
  File contents:
    """\\
    1
    2
    3
    """
  were NOT the same as the expected file contents:
    """\\
    1
    2
    """
  First difference was:
    strings differ on line 3 where we got:
      '3'
    but we expected:
      ''
  Called function 'write123' with arguments:
    filename = 'b.txt'
''',
        '''\
✗ {file}:13
  File contents:
    """\\
    1
    2
    3
    """
  were NOT the same as the expected file contents:
    """\\
    1
    2
    hello
    """
  First difference was:
    strings differ on line 3 where we got:
      '3'
    but we expected:
      'hello'
  Called function 'write123' with arguments:
    filename = 'b.txt'
''',
        "✓ {file}:23",
        '''\
✗ {file}:25
  File contents:
    """\\
    abc\\r
    def\\r
    """
  were NOT the same as the expected file contents:
    """\\
    abc
    def
    """
  First difference was:
    strings differ on line 1 where we got:
      'abc\\r'
    but we expected:
      'abc'
  Called function 'writeReturny' with arguments:
    filename = 'a.txt'
''',
        "✓ {file}:37",
        "✓ {file}:39",
        "✓ {file}:46",
        '''\
✗ {file}:48
  Result:
    'abc\\ndef'
  was NOT equivalent to the expected value:
    'abc\\ndef\\n'
  Test expression was:
    'abc\\ndef'
''',
    ],

    "code": [
        "✓ {file}:21",
        "✓ {file}:24",
        "✓ {file}:25",
        "✓ {file}:26",
        "✓ {file}:40",
        "✓ {file}:41",
        """\
✗ {file}:42
  Code does not contain the expected structure:
    at least 1 definition(s) of functionName
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: FunctionDef on line 10
  checked code in file '{full_file}'""",
        "✓ {file}:44",
        """\
✗ {file}:45
  Code does not contain the expected structure:
    at least 1 function definition(s) that also contain(s):
      at least 1 loop(s) or generator expression(s)
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: FunctionDef on line 10
  checked code in file '{full_file}'""",
        """\
✗ {file}:46
  Code does not contain the expected structure:
    at least 1 loop(s) or generator expression(s) that also contain(s):
      at least 1 function definition(s)
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: For on line 29
  checked code in file '{full_file}'""",
        """\
✗ {file}:47
  Code does not contain the expected structure:
    at least 1 while loop(s)
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: For on line 29
  checked code in file '{full_file}'""",
        "✓ {file}:48",
        "✓ {file}:50" if better_line_numbers else "✓ {file}:51",
        "✓ {file}:53" if better_line_numbers else "✓ {file}:54",
        "✓ {file}:56" if better_line_numbers else "✓ {file}:57",
        """\
✗ {file}:""" + ('59' if better_line_numbers else '60') + """
  Code does not contain the expected structure:
    at least 1 loop(s) or generator expression(s) that also contain(s):
      4 call(s) to print
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: For on line 29
  checked code in file '{full_file}'""",
        """\
✗ {file}:""" + ('62' if better_line_numbers else '63') + """
  Code does not contain the expected structure:
    at least 1 loop(s) or generator expression(s) that also contain(s):
      at least 4 call(s) to print
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: For on line 29
  checked code in file '{full_file}'""",
        "✓ {file}:65" if better_line_numbers else "✓ {file}:66",
        """\
✗ {file}:""" + ('68' if better_line_numbers else '69') + """
  Code does not contain the expected structure:
    at least 1 loop(s) or generator expression(s) that also contain(s):
      no call(s) to print
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: For on line 29
  checked code in file '{full_file}'""",
        "✓ {file}:71" if better_line_numbers else "✓ {file}:72",
        "✓ {file}:75" if better_line_numbers else "✓ {file}:76",
        """\
✗ {file}:""" + ('78' if better_line_numbers else '79') + """
  Code does not contain the expected structure:
    at least 1 if/else statement(s) or expression(s) that also contain(s):
      at least 1 operator '>'
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 1 partial match(es):
      Partial match: If on line 33
  checked code in file '{full_file}'""",
        "✓ {file}:81" if better_line_numbers else "✓ {file}:82",
        "✓ {file}:84" if better_line_numbers else "✓ {file}:85",
        "✓ {file}:90",
        "✓ {file}:91",
        "✓ {file}:92",
        """\
✗ {file}:93
  Code does not contain the expected structure:
    at least 1 constant 2.0
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 52 partial match(es):
""" + ("""\
      Partial match: Constant on line 1
      Partial match: Constant on line 7""" if better_line_numbers else """\
      Partial match: Str on line 3
      Partial match: NameConstant on line 7"""),  # not listing all 52...
        "✓ {file}:94",
        """\
✗ {file}:95
  Code does not contain the expected structure:
    at least 1 constant 5.0
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 52 partial match(es):
""" + ("""\
      Partial match: Constant on line 1
      Partial match: Constant on line 7""" if better_line_numbers else """\
      Partial match: Str on line 3
      Partial match: NameConstant on line 7"""),  # not listing all 52...
    ],

    "reverse_tracing": [
        # TODO
    ],

    "suites": [
        "✓ {file}:14",
        "✓ {file}:16",
        "✓ {file}:17",
        "✓ {file}:20",
        "✓ {file}:24",
        '''\
✗ {file}:26
  Printed lines:
    """\\
    4
    """
  were NOT the same as the expected printed lines:
    """\\
    5
    """
  First difference was:
    strings differ on line 1 where we got:
      '4'
    but we expected:
      '5'
  Called function 'f' with arguments:
    x = 4
    y = 5''',
        "✓ {file}:27",
        "✓ {file}:29",
        """\
-- Summary for suite 'B' --
1 of the 4 expectation(s) were NOT met:
  ✗ {file}:26
----""",
        """\
-- Summary for suite 'A' --
All 4 expectation(s) were met.
----""",
    ],

    "literals": [
        "✓ {file}:17",
        "✓ {file}:18",
        "✓ {file}:19",
        "✓ {file}:20",
        "✓ {file}:21",
        "✓ {file}:22",
        "✓ {file}:23" if better_line_numbers else "✓ {file}:24",
        "✓ {file}:27",
        "✓ {file}:28",
        "✓ {file}:29",
        "✓ {file}:30",
        "✓ {file}:31",
        "✓ {file}:32",
        "✓ {file}:33",
        "✓ {file}:34",
        """\
✗ {file}:36
  Code does not contain the expected structure:
    at least 1 literal [4, 5, 6]
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 6 partial match(es):
      Partial match: List on line 2
      Partial match: Tuple on line 3
      Partial match: List on line 6
      Partial match: List on line 7
      Partial match: Tuple on line 7
      Partial match: List on line 7
  checked code from block at {file}:16""",
        """\
✗ {file}:37
  Code does not contain the expected structure:
    at least 1 literal (1, 2, 3)
  Although it does partially satisfy the requirement:
    Requirement partially satisfied via 0 full and 6 partial match(es):
      Partial match: List on line 2
      Partial match: Tuple on line 3
      Partial match: List on line 6
      Partial match: List on line 7
      Partial match: Tuple on line 7
      Partial match: List on line 7
  checked code from block at {file}:16""",
        """\
✗ {file}:40
  Code does not contain the expected structure:
    at least 1 literal(s)
  checked code from block at {file}:39""",
        """\
✗ {file}:41
  Code does not contain the expected structure:
    at least 1 list literal(s)
  checked code from block at {file}:39""",
        """\
✗ {file}:42
  Code does not contain the expected structure:
    at least 1 tuple literal(s)
  checked code from block at {file}:39""",
        """\
✗ {file}:43
  Code does not contain the expected structure:
    at least 1 set literal(s)
  checked code from block at {file}:39""",
        """\
✗ {file}:44
  Code does not contain the expected structure:
    at least 1 dict literal(s)
  checked code from block at {file}:39""",
        "✓ {file}:47",
        "✓ {file}:48",
        "✓ {file}:49",
        "✓ {file}:50",
        "✓ {file}:51",
        "✓ {file}:54",
    ],

    "structure": [
        "✓ {file}:18",
        """\
✗ {file}:22
  Structure of the result:
    @0: [1, 2, @1, @0]
    @1: [3, 4]
  was NOT equivalent to the expected structure:
    @0: [1, 2, @1, @0]
    @1: [3, 4]
    @2: ['extra']
  Differences:
    did not find a match for list @2
  Called function 'f'
""",
        "✓ {file}:27",
        "✓ {file}:33",
        "✓ {file}:34",
        "✓ {file}:35",
        "✓ {file}:52",
        "✓ {file}:61",
        "✓ {file}:67",
        "✓ {file}:74",
        """\
✗ {file}:75
  Variable 'x' had structure:
    x: @0
    @0: [@1]
    @1: [1, 2]
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: [@1]
    @1: [1]
  Differences:
    list @1: list has 1 extra item(s)
  Ran code:
    x = [[1, 2]]
""",
        """\
✗ {file}:76
  Variable 'x' had structure:
    x: @0
    @0: [@1]
    @1: [1, 2]
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: [@1]
    @1: [1, 2, 3]
  Differences:
    list @1: list has 1 missing item(s)
  Ran code:
    x = [[1, 2]]
""",
        """\
✗ {file}:77
  Variable 'x' had structure:
    x: @0
    @0: [@1]
    @1: [1, 2]
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: [@1]
    @1: [3, 4]
  Differences:
    list @1 slot 0: value 1 differs from expected value 3
    list @1 slot 1: value 2 differs from expected value 4
  Ran code:
    x = [[1, 2]]
""",
        "✓ {file}:80",
        """\
✗ {file}:81
  Variable 'x' had structure:
    x: @0
    @0: (@1,)
    @1: (1, 2)
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: (@1,)
    @1: (1,)
  Differences:
    tuple @1: tuple has 1 extra item(s)
  Ran code:
    x = ((1, 2),)
""",
        """\
✗ {file}:82
  Variable 'x' had structure:
    x: @0
    @0: (@1,)
    @1: (1, 2)
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: (@1,)
    @1: (1, 2, 3)
  Differences:
    tuple @1: tuple has 1 missing item(s)
  Ran code:
    x = ((1, 2),)
""",
        """\
✗ {file}:83
  Variable 'x' had structure:
    x: @0
    @0: (@1,)
    @1: (1, 2)
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: (@1,)
    @1: (3, 4)
  Differences:
    tuple @1 slot 0: value 1 differs from expected value 3
    tuple @1 slot 1: value 2 differs from expected value 4
  Ran code:
    x = ((1, 2),)
""",
        "✓ {file}:91",
        "✓ {file}:96",
        "✓ {file}:101",
        """\
✗ {file}:105
  Variable 'x' had structure:
    x: @0
    @0: (@1, @1)
    @1: (1, 2)
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: (@1, @1)
    @1: (1, 2, 3)
  Differences:
    tuple @1: tuple has 1 missing item(s)
  Ran code:
    x = ((1, 2),)
    x = x + (x[0],)
    y = x[0]
    y = y + (3,)
""",
        """\
✗ {file}:110
  Variable 'x' had structure:
    x: @0
    @0: (@1, @1)
    @1: (1, 2)
  which was NOT structurally equivalent to to the expected structure:
    x: @0
    @0: (@3, @3)
    @3: (1, 2, 3)
  Differences:
    tuple @1: tuple has 1 missing item(s)
  Ran code:
    x = ((1, 2),)
    x = x + (x[0],)
    y = x[0]
    y = y + (3,)
"""
    ],

    "doctests":  [
        """\
✗ {file}:22
  Docstring was absent or empty.
  checked code of function 'a'
""",
        """\
✗ {file}:23
  Found only 0 distinct doctest example(s) (required 1).
  checked code of function 'a'
""",
        """\
✗ {file}:24
  No doctests were found.
  checked code of function 'a'
""",
        """\
✗ {file}:33
  Docstring was absent or empty.
  checked code of function 'b'
""",
        """\
✗ {file}:34
  Found only 0 distinct doctest example(s) (required 1).
  checked code of function 'b'
""",
        """\
✗ {file}:35
  No doctests were found.
  checked code of function 'b'
✓ {file}:44
""",
        """\
✗ {file}:45
  Found only 0 distinct doctest example(s) (required 1).
  checked code of function 'c'
""",
        """\
✗ {file}:46
  No doctests were found.
  checked code of function 'c'
""",
        "✓ {file}:61",
        "✓ {file}:62",
        "✓ {file}:63",
        "✓ {file}:64",
        """\
✗ {file}:65
  Found only 1 distinct doctest example(s) (required 2).
  checked code of function 'd'
""",
        "✓ {file}:76",
        """\
✗ {file}:77
  At {file}:72, output didn't match what the test expected. Expected:
    4
  Got:
    3
  checked code of function 'e'
""",
        "✓ {file}:92",
        "✓ {file}:93",
        "✓ {file}:94",
        """\
✗ {file}:95
  Found only 3 distinct doctest example(s) (required 4).
  checked code of function 'f'
""",
        "✓ {file}:96",
        "✓ {file}:96",
        "✓ {file}:96",
        "✓ {file}:114",
        "✓ {file}:115",
        """\
✗ {file}:116
  Found only 3 distinct doctest example(s) (required 4).
  checked code of function 'g'
""",
        "✓ {file}:117",
        "✓ {file}:117",
        "✓ {file}:117",
        "✓ {file}:119",
        "✓ {file}:120",
        """\
✗ {file}:122
  At {file}:104, output didn't match what the test expected. Expected:
    2
  Got:
    Unexpected exception:
      Traceback omitted
      NameError: name 'g' is not defined
  checked code of function 'g'
""",
        """\
✗ {file}:122
  At {file}:106, output didn't match what the test expected. Expected:
    3
  Got:
    Unexpected exception:
      Traceback omitted
      NameError: name 'g' is not defined
  checked code of function 'g'
""",
        """\
✗ {file}:122
  At {file}:108, output didn't match what the test expected. Expected:
    4
  Got:
    Unexpected exception:
      Traceback omitted
      NameError: name 'g' is not defined
  checked code of function 'g'
""",
        """\
✗ {file}:124
  At {file}:104, output didn't match what the test expected. Expected:
    2
  Got:
    Unexpected exception:
      Traceback omitted
      NameError: name 'g' is not defined
  checked code of function 'g'
""",
        """\
✗ {file}:124
  At {file}:106, output didn't match what the test expected. Expected:
    3
  Got:
    Unexpected exception:
      Traceback omitted
      NameError: name 'g' is not defined
  checked code of function 'g'
""",
        """\
✗ {file}:124
  At {file}:108, output didn't match what the test expected. Expected:
    4
  Got:
    Unexpected exception:
      Traceback omitted
      NameError: name 'g' is not defined
  checked code of function 'g'
""",
        "✓ {file}:139",
        "✓ {file}:140",
        """\
✗ {file}:141
  Found only 3 distinct doctest example(s) (required 4).
  checked code of function 'h'
""",
        "✓ {file}:142",
        "✓ {file}:142",
        """\
✗ {file}:142
  At {file}:135, output didn't match what the test expected. Expected:
    4
  Got:
    3
  checked code of function 'h'
""",
        "✓ {file}:157",
        """\
✗ {file}:158
  Found only 1 distinct doctest example(s) (required 2; ignored 2 duplicates).
  checked code of function 'i'
""",
        "✓ {file}:159",
        "✓ {file}:159",
        "✓ {file}:159",
        "✓ {file}:175",
        """\
✗ {file}:176
  At {file}:166, output didn't match what the test expected. Expected:
    3
  Got:
    2
  checked code of function 'j'
""",
        "✓ {file}:176",
        "✓ {file}:176",
        "✓ {file}:201",
        """\
✗ {file}:202
  Found only 2 distinct doctest example(s) (required 3).
  checked code of function 'k'
""",
        "✓ {file}:203",
        "✓ {file}:203",
        "✓ {file}:221",
        """\
✗ {file}:222
  Found only 3 distinct doctest example(s) (required 4).
  checked code of function 'l'
""",
        "✓ {file}:223",
        "✓ {file}:223",
        "✓ {file}:223",
        "✓ {file}:239",
        """\
✗ {file}:240
  Found only 3 distinct doctest example(s) (required 4).
  checked code of function 'm'
""",
        "✓ {file}:241",
        "✓ {file}:241",
        """\
✗ {file}:241
  At {file}:235, output didn't match what the test expected. Expected:
    '11'
  Got:
    Unexpected exception:
      Traceback omitted
      TypeError: can only concatenate str (not "int") to str
  checked code of function 'm'
""",
        "✓ {file}:264",
        """\
✗ {file}:265
  Found only 1 distinct doctest example(s) (required 2; ignored 4 duplicates).
  checked code of function 'n'
""",
        "✓ {file}:266",
        "✓ {file}:266",
        "✓ {file}:266",
        "✓ {file}:266",
        "✓ {file}:266",
        "✓ {file}:281",
        """\
✗ {file}:282
  Found only 1 distinct doctest example(s) (required 2).
  checked code of function 'o'
""",
        "✓ {file}:283",
        "✓ {file}:300",
        "✓ {file}:300",
        "✓ {file}:300",
        "✓ {file}:300",
        "✓ {file}:303",
        """\
✗ {file}:304
  Found only 4 distinct doctest example(s) (required 5).
  checked code of function 'p'
""",
        "✓ {file}:306",
        """\
✗ {file}:307
  Found only 3 matching distinct doctest example(s) (required 4).
  checked code of function 'p'
""",
        "✓ {file}:309",
        """\
✗ {file}:310
  Found only 1 matching distinct doctest example(s) (required 2).
  checked code of function 'p'
""",
        "✓ {file}:312",
        """\
✗ {file}:313
  Found only 1 matching distinct doctest example(s) (required 2).
  checked code of function 'p'
""",
        "✓ {file}:315",
        """\
✗ {file}:316
  Found only 2 matching distinct doctest example(s) (required 3).
  checked code of function 'p'
""",
        "✓ {file}:319",
        """\
✗ {file}:320
  Found only 1 matching distinct doctest example(s) (required 2).
  checked code of function 'p'
""",
        "✓ {file}:322",
        """\
✗ {file}:323
  Found only 2 matching distinct doctest example(s) (required 3).
  checked code of function 'p'
""",
        "✗ {file}:325",
        """\
  Found only 0 matching distinct doctest example(s) (required 1).
  checked code of function 'p'
""",
        "✓ {file}:327",
        """\
✗ {file}:328
  Found only 1 matching distinct doctest example(s) (required 2).
  checked code of function 'p'
""",
        "✓ {file}:362",
        "✓ {file}:363",
        """\
✗ {file}:364
  Found only 3 distinct doctest example(s) (required 4; ignored 1 duplicates).
  checked code from block at {file}:332
""",
        "✓ {file}:365",
        "✓ {file}:365",
        "✓ {file}:365",
        "✓ {file}:365",
        """\
✗ {file}:370
  Docstring was absent or empty.
  checked code from block at {file}:368
""",
        """\
✗ {file}:371
  Found only 0 distinct doctest example(s) (required 1).
  checked code from block at {file}:368
""",
        """\
✗ {file}:372
  No doctests were found.
  checked code from block at {file}:368
""",
        """\
✗ {file}:377
  Docstring was absent or empty.
  checked code from block at {file}:375
""",
        "✓ {file}:378",
        """\
✗ {file}:379
  Found only 1 distinct doctest example(s) (required 2).
  checked code from block at {file}:375
""",
        "✓ {file}:380",
        """\
✗ {file}:384
  At code block from {file}:383:4, output didn't match what the test expected. Expected:
    4
  Got:
    5
  checked code from block at {file}:383
""",
        "✓ {file}:390",
        "✓ {file}:391",
        "✓ {file}:391",
        "✓ {file}:391",
        "✓ {file}:391",
        "✓ {file}:391",
        "✓ {file}:392",
        """\
✗ {file}:393
  Found only 5 distinct doctest example(s) (required 6).
  checked code in file 'doc_example.py'
""",
        "✓ {file}:394",
        """\
✗ {file}:395
  Found only 2 matching distinct doctest example(s) (required 3).
  checked code in file 'doc_example.py'
"""
    ],
    "memoryReports": [
        "✓ {file}:22",
        "✓ {file}:23",
    ]
}

STDOUT_EXPECT = {
    "catch_and_release": [
        "one Z!",
        "Re-providing input was blocked.",
        "Hello",
        "two Z!"
    ],

    "code": [
        "0",
        "1",
        "2",
        "3"
    ],

    "suites": [
        '3',
        'a',
        """\
Outcomes in suite A:
(True, '{file}:14', '✓ {file}:14')
(True, '{file}:16', '✓ {file}:16')
(True, '{file}:17', '✓ {file}:17')
(True, '{file}:20', '✓ {file}:20')""",
        '''\
Outcomes in suite B:
(True, '{file}:24', '✓ {file}:24')
(False, '{file}:26', '✗ {file}:26\\n  Printed lines:\\n    """\\\\\\n    4\\n    """\\n  were NOT the same as the expected printed lines:\\n    """\\\\\\n    5\\n    """\\n  First difference was:\\n    strings differ on line 1 where we got:\\n      \\\'4\\\'\\n    but we expected:\\n      \\\'5\\\'\\n  Called function \\\'f\\\' with arguments:\\n    x = 4\\n    y = 5')
(True, '{file}:27', '✓ {file}:27')
(True, '{file}:29', '✓ {file}:29')''', # noqa E501
        """\
Outcomes in suite A (again):
(True, '{file}:14', '✓ {file}:14')
(True, '{file}:16', '✓ {file}:16')
(True, '{file}:17', '✓ {file}:17')
(True, '{file}:20', '✓ {file}:20')
(True, '{file}:46', '✓ {file}:46')""",
        "No more outcomes in suite A: []",
        "No more outcomes in suite B: []",
        "No more suite B.",
    ],

    "memoryReports": [
        """\
words: @0
pair: @3
@0: [@1, @2]
@3: [@0, @0]
@1: 'hi'
@2: 'bye'
""",
        """\
pair: @0
words: @1
knot: @4
@0: [@1, @1]
@1: [@2, @3]
@4: [@0, @1, @4]
@2: 'hi'
@3: 'bye'
""",
    ]
}


def run_example(mname, inputs=[]):
    """
    Runs a module and captures stderr and stdout, returning a tuple
    containing the imported module, the captured stderr string, and the
    captured stdout string. The given input strings are provided as stdin
    during the run.
    """
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    old_stdin = sys.stdin
    old_print_to = optimism.PRINT_TO
    sys.stderr = io.StringIO()
    sys.stdout = io.StringIO()
    sys.stdin = io.StringIO('\n'.join(inputs) + '\n')
    optimism.PRINT_TO = sys.stderr

    filePath = os.path.abspath(mname + '.py')

    try:
        spec = importlib.util.spec_from_file_location(mname, filePath)
        module = importlib.util.module_from_spec(spec)
        # Note we skip adding it to sys.modules
        spec.loader.exec_module(module)
        errOut = sys.stderr.getvalue()
        stdOut = sys.stdout.getvalue()

    finally:
        sys.stderr = old_stderr
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        optimism.PRINT_TO = old_print_to

    return (module, errOut, stdOut)


def test_all():
    """
    Tests each example file. The `examples` directory must be in the
    same place that this `test_examples.py` file lives.
    """
    os.chdir(os.path.join(os.path.dirname(__file__), "examples"))
    sys.path.insert(0, '.')
    for (mname, inputs) in EXAMPLES:
        optimism.detailLevel(0)
        optimism.deleteAllTestSuites()
        optimism.colors(False)
        module, output, stdout = run_example(mname, inputs)
        # Replace tracebacks with generic forms so we can match on
        # specific errors being reported while ignoring the files & lines
        # where they are reported.
        stdout = re.sub(
            r"Traceback \(most recent call last\):.*?^([ a-zA-Z]*Error:)",
            "Traceback omitted\n\\1",
            stdout,
            flags=re.MULTILINE | re.DOTALL
        )
        output = re.sub(
            r"Traceback \(most recent call last\):.*?^([ a-zA-Z]*Error:)",
            "Traceback omitted\n\\1",
            output,
            flags=re.MULTILINE | re.DOTALL
        )
        #output = re.sub(r"Traceback \(most recent call last\).*?NameError:", "HAHAHA", output, flags=re.MULTILINE | re.DOTALL)
        # Scrub line numbers from tracebacks so our expectations don't
        # become hopelessly fragile
        stdout = re.sub(r", line \d+,", ", line X,", stdout)
        output = re.sub(r", line \d+,", ", line X,", output)
        for ex in EXPECTATIONS[mname]:
            exp = ex.format(
                file=os.path.basename(module.__file__),
                dir=(
                    os.path.split(module.__file__)[0] + '/'
                    if better_line_numbers
                    else ''
                ),
                full_file=module.__file__,
                opt_file=optimism.__file__,
            )
            # Redundant, but makes issues easier to diagnose
            for line in exp.splitlines():
                if line not in output:
                    print("\n\nLINE:\n" + line)
                    print("\n\nOUTPUT:\n" + output)
                assert (line in output), (line, output)
            if exp not in output:
                print("\n\nEXP:\n" + exp)
                print("\n\nOUTPUT:\n" + output)
            assert (exp in output), (exp, output)
        if mname in STDOUT_EXPECT:
            for ex in STDOUT_EXPECT[mname]:
                exp = ex.format(
                    file=os.path.basename(module.__file__),
                    dir=os.path.split(module.__file__)[0],
                    full_file=module.__file__,
                    opt_file=optimism.__file__,
                )
                for line in exp.splitlines():
                    assert (line in stdout), stdout
                assert (exp in stdout), stdout
    os.chdir("..")
