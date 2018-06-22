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

#module.set_RX_out_emphasis(2,2,2,2)

#module.CDR_enable()

module.high_power_enable()

module.close_handle()

#module.set_CTLE_fixed(3,3,3,3)
#module.set_RX_out_amplitude(2,2,2,2)
#module.set_RX_out_emphasis(0,0,0,0)

#print module.get_CTLE()

#print module.get_RX_out_amplitude()

#print module.get_RX_out_emphasis()

#print module.poller()
