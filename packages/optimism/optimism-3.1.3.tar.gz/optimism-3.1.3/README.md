# `optimism`

A very small & simple unit-testing framework designed to provide all the
basic necessities to beginner programmers as simply as possible.

Designed by Peter Mawhorter.


## Dependencies

Works on Python versions 3.7 and up, with 3.9+ recommended.


## Installing

To install from PyPI, run the following command on the command-line:

```sh
python3 -m pip install optimism
```

Once it's installed, you can run the tests using:

```sh
pytest --doctest-modules optimism.py
pytest test_examples.py
```

## Usage

Use the `testFunction`, `testFunctionMaybe`, `testFile`, `testBlock`,
and/or `testThisNotebookCell` functions to establish test managers for
specific pieces of code. Then use those managers' `checkCodeContains`
methods to check for the presence/absence of certain code constructs (see
the `ASTRequirement` class) or use the `case` method to establish a test
case w/ specific inputs (one manager can support multiple derived cases
w/ different inputs). Finally, use methods of a test case like
`checkResult` or `checkPrintedLines` to check for specific behavior.

See
[the documentation](https://cs.wellesley.edu/~pmwh/optimism/docs/optimism)
for more details on how to use it and what each function does.

## Changelog

See
[the documentation](https://cs.wellesley.edu/~pmwh/optimism/docs/optimism#changelog).
