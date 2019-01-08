from Modules.qsfp28 import *
import os
import sys

module=qsfp28()


print module.get_vendor_name()
print module.get_serial_number()
print module.get_temperature()
print module.get_voltage()
print module.get_TX_power()
print module.get_vendor_PN()
print module.get_status()


module.high_power_enable()

time.sleep(1)

module.set_CTLE_fixed(8,8,8,8)

time.sleep(1)

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

module.read_all_mem()

module.read_all_mem()

time.sleep(1)

module.single_write(0x56,0x00)