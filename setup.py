#!/usr/bin/env python
from setuptools import setup
from os import path

long_description = """
# PyMBR

PyMBR is a simple module that allows the user to parse, manipulate or create MBR/Bootsectors easily.

  - Parse full MBR dump
  - Parse parts of the MBR such as the partition table.
  - Change the bootcode or the artition table values.
  - Compose the changes made into a a new MBR binary string.

## Installation
``` sh
python setup.py install
```

## Sample usage - Creating a simple MBR 
``` python
import pymbr
mbr = pymbr.MBR()
mbr.bootcode = pymbr.Bootcode.ZOIDBERG
mbr.partitionTable = pymbr.PartitionTable.parse('\x00' * 64)
mbr.signature = 0xaa55
bin = mbr.compose()
with open('mbr.bin', 'wb') as file:
    file.write(bin)
```
## TODOs:
* Add more common filesystems to the Filesystem class
* Add common MBR bootcode to he Bootcode class
* Add LBA to CHS converion
* Add overlapping partition prevention
* Tests?

"""

setup(
	name = 'pymbr',
	version = '1.0.2',
	description = 'A python module to manipulate and create MBRs.',
	long_description = long_description,
	url = 'https://github.com/0xGiddi/pymbr',
	packages = ['pymbr'],
	package_dir = { 'pymbr' : 'pymbr' },
	license = 'GPLv3',
	author = 'Gideon S. (0xGiddi)',
	author_email = 'elmocia@gmail.com',
	classifiers = [
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Intended Audience :: Information Technology',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft',
		'Topic :: System :: Boot',
		'Topic :: System :: Operating System',
		'Topic :: System :: Recovery Tools',
		'Topic :: System :: Systems Administration',
		'Development Status :: 4 - Beta',
		'Topic :: Utilities',
	]
)

