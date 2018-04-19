import pymsgbox
import pymsgbox
from Modules.sfp28 import *
from Instruments.Fluke_8846A import *
from Instruments.KikusuiPBZ20 import *
from Instruments.Agilent33600A import *
from Instruments.DLI100G40G import *
import time
import os

module=sfp28()

TE=DLI100G40G('10.58.241.161','8090')
mm=Fluke_8846A(12)
gen.set_hi_z(1)

#module configuration
M_SN=module.get_serial_number()
M_VN=module.get_vendor_name()

print 'Module under test id: ' + M_VN + ' ' + M_SN + '\n'


log=open(Test_3_M_VN + '_' + M_SN + time.strftime('%H_%M_%d_%m_%Y.txt'),"w")
head="LOS_status,Voltage_DDM,Temperature_DDM,RX1,BIAS1,TX1,Multimeter,TIMESTAMP" + '\n'
log.write(head)

now = time.strftime("%c")
print "Test Started at " + now

TE.start_counters()

for i in range (0,180): # minutes of test, test duration in minutes
	print "Minute n: "+str(i)+'\n'
	for k in range (1,30):
		poll=module.poller()
		volt_mm=mm.get_voltage()
		timestamp=time.strftime('%H_%M_%S')
		log.write(poll +',' +str(volt_mm)+ ',' + timestamp +'\n')
		time.sleep(1.94)
		
TE.stop_counters()
traffic_res=TE.get_results()
print "Alarms on DLI Test Set"
print TE.get_alarms()
print "Events on DLI Test Set"
TE.get_events()
print "I2C Errors occured"
print module.get_i2c_counter()
TE.logout()
log.close()


now = time.strftime("%c")
print "Test Finished at " + now









