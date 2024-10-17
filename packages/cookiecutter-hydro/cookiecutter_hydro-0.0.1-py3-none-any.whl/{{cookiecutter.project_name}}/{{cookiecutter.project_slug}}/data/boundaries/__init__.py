"""Path for the data:

Attributes:

    boundaries (Traversable): base path of the boundary condition directory.

"""

from importlib import resources
from importlib.abc import Traversable

boundaries: Traversable = resources.files(__name__)
"""The whole directory of test groundwater sensor data."""

processed: Traversable = boundaries.joinpath("processed")
"""Processed boundary condition data."""


raw: Traversable = boundaries.joinpath("raw")
"""Raw boundary condition data."""
