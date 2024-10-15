"""
This package init just imports everything from optimism.py, including
explicitly the version number (which otherwise would be skipped since it
starts with '_'). That way, importing optimism-the-package is the same as
importing optimism-the-file, except that private variables are not
exported by the package. So you can distribute the package OR just the
optimism.py file and both should work the same.
"""

from .optimism import *

# Setuptools versions on Python 3.10 won't allow us to just import the
# version from optimism, but we want the version to be defined in that
# file so that a single-file distribution is equivalent to this packaged
# distribution. So we define a version here as well, but...
__version__ = "3.1.3"

# ...then we assert it matches so testing will catch it if I forget to
# keep them in sync before a release. T_T
from .optimism import __version__ as match
assert __version__ == match
