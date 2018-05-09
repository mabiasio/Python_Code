from Modules.qsfp28 import *
import os
import sys


module=qsfp28()



print module.get_serial_number()
print module.get_voltage()
print module.get_temperature()

module.read_all_mem()

#module.CDR_enable()




