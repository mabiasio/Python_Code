from Modules.qsfp_dd_tl import *
import os
import sys


module=qsfp_dd_tl()



print module.get_serial_number()
print module.get_voltage()
print module.get_temperature()
module.set_cutoff(90)



#module.set_dissipation_5()
#time.sleep(10)
#module.set_dissipation_7()
#time.sleep(10)
module.set_dissipation_9()
time.sleep(10)
#module.set_dissipation_11()
#time.sleep(10)
#module.set_dissipation_13()
#time.sleep(10)
#module.set_dissipation_15()
#time.sleep(10)
module.set_dissipation_off()


