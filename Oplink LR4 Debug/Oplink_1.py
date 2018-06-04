from Modules.qsfp28 import *
import os
import sys


module=qsfp28()


module.single_write(0x62,0xF0)

#module.read_all_mem()

time.sleep(0.1)

module.set_page(0)

module.single_write(0x62,0xFF)

module.read_all_mem()

module.read_all_mem()

module.set_page(0)

module.single_write(0x56,0x00)

module.read_all_mem()

module.read_all_mem()

module.read_all_mem()

module.set_page(0)

module.set_page(3)

module.set_page(3)

module.single_read(0xF1)

module.single_write(0xF1,0x0F)

module.read_all_mem()

module.read_all_mem()

module.read_all_mem()

module.read_all_mem()

module.read_all_mem()

module.read_all_mem()

print module.get_i2c_counter()

#End Sequence