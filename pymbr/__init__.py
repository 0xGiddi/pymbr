"""
    pymbr
    
    A python module to manipulate and create MBRs.
    :copyright: (c) 2017 by Gideon S. (0xGiddi)
    :license: GPLv3, see LICENSE file for more details.
"""

__version__ = "1.0.2"

from .bootrecord import *
from .bootcode import *
from .filesystem import Filesystem
from .partition import *
