import pymsgbox
from Modules.qsfp28 import *
from Instruments.Fluke_8846A import *
from Instruments.KikusuiPBZ20 import *
from Instruments.Agilent33600A import *
from Instruments.DLI100G40G import *
import time
import os


module=qsfp28()

print module.get_vendor_name()
print module.get_serial_number()
print module.get_temperature()
print module.get_voltage()
print module.get_TX_power()
print module.get_vendor_PN()
print module.get_status()


#module.high_power_enable()
#time.sleep(1)
#module.set_CTLE_fixed(8,8,8,8)
#module.set_CTLE_fixed(3,3,3,3)
#module.set_RX_out_amplitude(2,2,2,2)
#module.set_RX_out_emphasis(0,0,0,0)

#print module.get_CTLE()

#print module.get_RX_out_amplitude()

#print module.get_RX_out_emphasis()

print module.poller()

module.close_handle()
