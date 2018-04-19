from Modules.qsfp28 import *
import os
import sys


module=qsfp28()



print module.get_serial_number()
print module.get_voltage()
print module.get_temperature()
#module.set_cutoff(90)

module.CDR_enable()




