"""
    pymbr
    
    A python module to manipulate and create MBRs.
    :copyright: (c) 2017 by Gideon S. (0xGiddi)
    :license: GPLv3, see LICENSE file for more details.
"""
from __future__ import print_function
import struct
from .bootrecord import *

__all__ = ['PartitionTable', 'PartitionEntry', 'CHSTuple']


class CHSTuple(object):
	""" CHS disk geometry tuple"""
	__slots__ = ['cylinder', 'head', 'sector']
	chsStruct = struct.Struct('<3B')

	def __init__(self, head, sect, cyl):
		""" C'tor - Create CHStumple from specified values"""
		self.head = head
		self.sector = sect
		self.cylinder = cyl

	@staticmethod
	def parse(chsData):
		"""" Parse a CHS tuple from binary form """
		if len(chsData) != 3: raise ValueError("CHS Data must be 3 bytes in size")
		unpacked = CHSTuple.chsStruct.unpack(chsData)
		return CHSTuple(unpacked[0], unpacked[1] & 63, unpacked[2] | ((unpacked[1] >> 6) << 8))


	def compose(self):
		""" Compose a CHS binary tuple to binary form """
		self.validate()
		return self.chsStruct.pack(self.head, self.sector | ((self.cylinder >> 8) << 6), self.cylinder & 255)

	def isBeyondLimit(self):
		""" Check if the CHS tuple is over the 8.4GB limit """
		return (self.cylinder >= 1023) and (self.head >= 254) and (self.sector >= 63)


	def validate(self):
		""" Validate the CHS tuple values"""
		if not 0 <= self.head <= 254:
			raise ValidationError("Head value must be between 0 and 254")
		if not 0 <= self.sector <= 63:
			raise ValidationError("Sector value must be between 0 and 63")
		if not 0 <= self.cylinder <= 1023:
			raise ValidationError("Cylinder value must be between 0 and 1023")


	def __repr__(self):
		return "<{cls} C:{cyl}, H:{head}, S:{sect}>".format(cls=type(self).__name__ , cyl=self.cylinder, head=self.head, sect=self.sector)

	__str__ = __repr__


class PartitionEntry(object):
	__slots__ = ['bootflag', 'startCHS', 'type', 'endCHS', 'lba', 'size']
	SECTOR_SIZE = 512
	MAX_LBA = 4294967295
	entryStruct = struct.Struct('<B3sB3sLL')

	def __init__(self, lba, size):
		""" C'tor - Create a new disk partition entry"""
		self.lba = lba
		self.size = size

	@staticmethod
	def parse(entryData):
		""" Parse a disk partition entry from binary form """
		if len(entryData) != 16:
			raise ValueError("Partition data should me 16 bytes in size")
		unpacked = PartitionEntry.entryStruct.unpack(entryData)
		ret = PartitionEntry(unpacked[4], unpacked[5])
		ret.bootflag = True if unpacked[0] == 0x80 else False
		ret.startCHS = CHSTuple.parse(unpacked[1])
		ret.type = unpacked[2]
		ret.endCHS = CHSTuple.parse(unpacked[3])
		return ret
		

	def compose(self):
		""" Compose a disk partition entry into binary form """
		self.validate()
		bootable = 0x80 if self.bootflag == True else 0x00
		return self.entryStruct.pack(bootable, self.startCHS.compose(), self.type, self.endCHS.compose(), self.lba, self.size)


	def validate(self):
		""" Validate the current disk partition entry"""
		self.startCHS.validate()
		self.endCHS.validate()

		if not 0 <= self.type <= 255:
			raise ValidationError("Type value must be between 0 and 255")
		if not (0 <= self.size <= self.MAX_LBA) or not (0 <= self.size <= self.MAX_LBA):
			raise ValidationError("Partition start/size must be between 0 and 4294967295 sector/s")
		# TODO: Add LBA start and size collition detection
			#raise ValidationError("Partition starts inside itself")

	def realSize(self):
		""" REturns he real size of he disk in bytes """
		return self.size * self.SECTOR_SIZE

	
	def __repr__(self):
		return "<{cls} LBA:{lba}, Size:{size}, Boot:{boot}, Type:{type}>".format(cls=type(self).__name__ , lba=self.lba, size=self.size, type=self.type, boot=self.bootflag)

	__str__ = __repr__



class PartitionTable(object):
	__slots__ = ['partitions']
	def __init__(self):
		self.partitions = {}


	@staticmethod
	def parse(tableData):
		""" Parse a partition table from binary form """
		if (len(tableData) / 16) not in [1,2,3,4]:
			raise ValueError("Partiton table should be multiples of 16 in size")
		partitions = {}
		for idx in xrange(0, len(tableData), 16):
			partitions[idx / 16] = PartitionEntry.parse(tableData[idx:idx + 16])

		table = PartitionTable()
		table.partitions = partitions
		return table

	def compose(self):
		""" Compose a partition table into binary form """
		self.validate()
		ret = r""
		for i, partition in self.partitions.items():
			partition.validate()
			ret += partition.compose()
		return ret + ('\x00' * (64 - len(ret)))


	def validate(self):
		""" Validate the disk partition table """
		bootPartitionCount = 0
		for i, partition in self.partitions.items():
			if partition.bootflag:
				bootPartitionCount += 1

		if bootPartitionCount > 1:
			print("Warning: Multiple boot parition defined")
		elif bootPartitionCount == 0:
			print("Warining: No boot partition defined")


	def getBootPartition(self):
		"""" Reurn the first partition that has thr bootflag set """
		for k,v in self.partitions.items():
			if v.bootflag:
				return v


	def __repr__(self):
		return "<{cls} Partitions:{partNum}>".format(cls=type(self).__name__ ,partNum=len(self.partitions))

	__str__ = __repr__
