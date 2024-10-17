"""Path for the data:

Attributes:

    output (Traversable): base path of the data directory.

"""

from importlib import resources
from importlib.abc import Traversable

output: Traversable = resources.files(__name__)
"""All files in the output directory."""
