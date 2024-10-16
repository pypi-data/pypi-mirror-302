"""
ggps library
"""

__author__ = "Chris Joakim <christopher.joakim@gmail.com>"
__version__ = "0.5.0"

AUTHOR = __author__
VERSION = __version__

DEFAULT_RUN_WALK_SEPARATOR_CADENCE = 150

from ggps.counter import Counter
from ggps.trackpoint import Trackpoint
from ggps.base_handler import BaseHandler
from ggps.gpx_handler import GpxHandler
from ggps.path_handler import PathHandler
from ggps.tcx_handler import TcxHandler
