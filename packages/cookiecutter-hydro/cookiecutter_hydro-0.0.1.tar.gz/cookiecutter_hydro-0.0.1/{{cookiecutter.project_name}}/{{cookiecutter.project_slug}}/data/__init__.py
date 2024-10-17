"""Path for the data:

Attributes:

    data (Traversable): base path of the data directory.

"""

from importlib import resources
from importlib.abc import Traversable

data: Traversable = resources.files(__name__)
"""The whole directory of test groundwater sensor data."""
