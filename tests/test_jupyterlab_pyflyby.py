"""
Jupyterlab-pyflyby extension related test

Some of these test do not need the full extension installed so we put them here.
"""

from pyflyby._comms import _reformat_helper, run_tidy_imports
import pytest


# insert between marker
a = (
    """
import before as   b
# THIS CELL WAS AUTO-GENERATED BY PYFLYBY
import middle as m

# END AUTO-GENERATED BLOCK
import after as  f

""",
    "import numpy as np",
    """
import before as b
# THIS CELL WAS AUTO-GENERATED BY PYFLYBY
import middle as m
import numpy as np

# END AUTO-GENERATED BLOCK
import after as f

""",
)

# there are no markers
b = (
    """
""",
    "import numpy as np",
    """
import numpy as np

""",
)

# import exists before marker, but will still be inserted.
# this is non optimal, but expected if the cell has not been executed
c = (
    """
import numpy as np
# THIS CELL WAS AUTO-GENERATED BY PYFLYBY
# END AUTO-GENERATED BLOCK

""",
    "import numpy as np",
    """
import numpy as np
# THIS CELL WAS AUTO-GENERATED BY PYFLYBY
import numpy as np

# END AUTO-GENERATED BLOCK

""",
)


@pytest.mark.parametrize(
    "origin,imports,expected",
    [a, b, c],
)
def test_reformat_with_markers(origin, imports, expected):
    """
    Here we test that import are added to code between markers, and
    that before/after markers are properly reformatted.
    """
    assert str(_reformat_helper(origin, ["import numpy as np"])) == expected

code_block = """
from os import *
print(getcwd())

from deshaw.djs import Chart, TidyReport
from deshaw.djs import Chart
Chart(range(10)).show()
"""

expected_output = """
from os import getcwd
print(getcwd())

from deshaw.djs import Chart
Chart(range(10)).show()
"""

@pytest.mark.parametrize(
    "code_block",
    [code_block]
)
def test_tidy_imports(code_block):
    code_post_tidy_imports = run_tidy_imports(code_block)
    assert code_post_tidy_imports == expected_output