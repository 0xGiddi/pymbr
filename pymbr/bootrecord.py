"""
    pymbr
    
    A python module to manipulate and create MBRs.
    :copyright: (c) 2017 by Gideon S. (0xGiddi)
    :license: GPLv3, see LICENSE file for more details.
"""

import struct
from .partition import PartitionTable

__all__ = ['MBR', 'ValidationError']

class ValidationError(Exception):
	""" Base class for errors raised while validating mbr objects. """
	pass

class MBR(object):
	"""
	The MBR object represents a wrapper for all the MBR components.
	"""
	__slots__ = ['bootcode', 'partitionTable', 'signature', '_data']
	mbrStruct = struct.Struct('<446B64sH')
	def __init__(self):
		""" C'tor - Create a blank MBR object """
		self.bootcode = {}
		self.partitionTable = None
		self.signature = None

	@staticmethod
	def parse(mbrData):
		""" Parses MBRs raw data into MBR object """
		if len(mbrData) != 512:
			raise ValueError("MBR data must be 512 bytes in size")
		unpacked = MBR.mbrStruct.unpack(mbrData)
		mbr = MBR()
		mbr.bootcode = list(unpacked[:446])
		mbr.partitionTable = PartitionTable.parse(unpacked[446])
		mbr.signature = unpacked[-1]
		return mbr

	
	def isValidSignature(self):
		""" Validate the MBRs signature """
		return self.signature == 0xaa55


	def compose(self):
		""" Compose a MBR binary string from the MBR object"""
		self.validate()
		self.bootcode = self._padBootcode()
		return self.mbrStruct.pack(*(self.bootcode + [self.partitionTable.compose()] + [self.signature]))

	def _padBootcode(self):
		""" Pad bootcode with nulls if under 446 bytes long """
		return list(self.bootcode) + [0] * (446 - len(self.bootcode))



	def validate(self):
		""" Preform validation of the MBR object and its components"""
		self.partitionTable.validate()
		if len(self.bootcode) > 446:
			raise ValidationError("Bootcode must be 446 bytes or less")
		if not self.isValidSignature():
			raise ValidationError("MBR has incorrect signature.")

	def __repr__(self):
		return "<{cls} Bootcode length:{bootLen}, Sig:{sig}>".format(cls=type(self).__name__ ,bootLen=len(self.bootcode), sig=self.signature)

	__str__ = __repr__




