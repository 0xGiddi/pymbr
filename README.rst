PyMBR
=====

PyMBR is a simple module that allows the user to parse, manipulate or
create MBR/Bootsectors easily.

-  Parse full MBR dump
-  Parse parts of the MBR such as the partition table.
-  Change the bootcode or the artition table values.
-  Compose the changes made into a a new MBR binary string.

Installation
------------

.. code:: sh

    python setup.py install

**or**

.. code:: sh

    pip install pymbr

Sample usage - Creating a simple MBR
------------------------------------

.. code:: python

    import pymbr
    mbr = pymbr.MBR()
    mbr.bootcode = pymbr.Bootcode.ZOIDBERG
    mbr.partitionTable = pymbr.PartitionTable.parse('\x00' * 64)
    mbr.signature = 0xaa55
    bin = mbr.compose()
    with open('mbr.bin', 'wb') as file:
        file.write(bin)

TODOs:
------

-  Add more common filesystems to the Filesystem class
-  Add common MBR bootcode to he Bootcode class
-  Add LBA to CHS converion
-  Add overlapping partition prevention
-  Tests?
