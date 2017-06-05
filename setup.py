#!/usr/bin/env python
from setuptools import setup
from os import path

this = path.abspath(path.dirname(__file__))
with open(path.join(this, 'README.md')) as readme:
	long_description = readme.read()

setup(
	name = 'pymbr',
	version = '1.0.0',
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
		'Intended Audience :: Information Technology'
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
		'Topic :: Utilities'
	]
)

