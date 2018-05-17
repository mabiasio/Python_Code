from Modules.qsfp28 import *
import os
import sys


module=qsfp28()


module.read_all_mem()

module.read_all_mem()

module.read_all_mem()

#read all mem tree times

module.set_page(0)

module.set_page(0)

module.set_page(0)

#tree times set page

module.single_write(0x56,0x0F)

module.read_all_mem()

module.set_page(0)

module.set_page(3)

module.set_page(3)

module.single_write(0xF1,0xF0)

module.read_all_mem()

module.set_page(0)

module.set_page(0)

module.set_page(0)

module.single_read(0x81)

module.single_read(0x5D)

module.single_write(0x5D,0x01)

module.single_read(0x5D)

module.set_page(0)

module.set_page(3)

module.set_page(3)

module.single_write(0xEE,0x22)

module.set_page(3)

module.single_write(0xEF,0x22)

module.set_page(0)

module.single_read(0xC1)

module.set_page(3)

module.single_read(0xF1)

module.single_write(0xF1,0xFF)

module.single_read(0xE5)

module.set_page(3)

module.single_write(0xEC,0x00)

module.set_page(3)

module.single_write(0xED,0x00)

module.set_page(3)

module.single_write(0xEE,0x22)

module.set_page(3)

module.single_write(0xEF,0x22)

module.read_all_mem()

module.read_all_mem()

module.read_all_mem()

module.set_page(0)

module.set_page(0)

module.set_page(0)

module.single_write(0x62,0xF0)

module.read_all_mem()

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




































