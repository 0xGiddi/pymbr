"""
    pymbr
    
    A python module to manipulate and create MBRs.
    :copyright: (c) 2017 by Gideon S. (0xGiddi)
    :license: GPLv3, see LICENSE file for more details.
"""

__all__ = ['Filesystem']

class Filesystem:
	EMPTY  = 0x00
	FAT_12 = 0x01
	FAT_16 = 0x06
	NTFS   = 0x07
	FAT_32 = 0X0b
	FAT_32_LBA = 0x0c
	EXTENDED_LBA = 0x0f

	# TODO: Add common filesystem types
