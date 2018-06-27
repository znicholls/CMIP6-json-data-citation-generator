"""
Thank you https://stackoverflow.com/a/17981937
"""

import sys
from contextlib import contextmanager
try: # tweak to make python3 and python2 compatible
    from StringIO import StringIO
except ImportError:
    from io import StringIO

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
