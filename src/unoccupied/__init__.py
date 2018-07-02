"""Unoccupied - Find unoccupied name."""

from .main import unoccupied
from .main import UnoccupiedNameNotFound
from .namefinder import NumberNameFinder
from .namefinder import FileNameFinder

__version__ = '0.1.2'

__all__ = ['unoccupied',
           'UnoccupiedNameNotFound',
           'NumberNameFinder',
           'FileNameFinder']
