from Modules.qsfp28 import *
import os
import sys


module=qsfp28()



print module.get_serial_number()
print module.get_voltage()
print module.get_temperature()

print module.get_RX_power()

#module.CDR_enable()




