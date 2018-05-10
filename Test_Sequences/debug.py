from Modules.qsfp28 import *
import os
import sys


module=qsfp28()



#module.CDR_disable()

#time.sleep(2)

#module.CDR_enable()

print module.get_serial_number()
print module.get_voltage()
print module.get_temperature()

print module.get_RX_power()

print module.poller()

#module.CDR_enable()




