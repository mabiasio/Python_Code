from Modules.CFP2 import *

module = cfp2()


print module.get_temperature()
print module.get_voltage()
print module.get_SN()
print module.get_vendor_name()

module.set_ctle(2,2,2,2)
print module.get_ctle()
print module.get_TX_power()
print module.get_RX_power()