import pymsgbox
from Modules.qsfp28 import *
from Instruments.Fluke_8846A import *
from Instruments.KikusuiPBZ20 import *
from Instruments.Agilent33600A import *
from Instruments.DLI100G40G import *
import time
import os

module=qsfp28()
psu=KikusuiPBZ20('10.58.241.170')
gen=Agilent33600A('10.58.241.171')
TE=DLI100G40G('10.58.241.161','8090')
mm=Fluke_8846A(12)

#print PSU and Wafeform Generator IDs

psu.identification()
gen.identification()

gen.output_off(1)
gen.output_off(2)



# PSU settings 3,3 VDC + external signal
psu.set_signal_source('BOTH')
psu.set_voltage('3.42')
psu.output_on()
time.sleep(1)



#module configuration
M_SN=module.get_serial_number()
M_VN=module.get_vendor_name()

print 'Module under test id: ' + M_VN + ' ' + M_SN + '\n'

#Pseudo-initialization sequence
time.sleep(0.5)
module.high_power_enable()
time.sleep(0.5)
module.CDR_enable()
time.sleep(0.5)
module.TX_enable()
module.set_CTLE_adaptive_disable()
module.set_CTLE_fixed(3,3,3,3)
module.set_RX_out_emphasis(2,2,2,2)
module.set_page(0)
time.sleep(0.5)

log=open("Test_4_LV_qsfp28_"+ M_VN + '_' + M_SN + time.strftime('%H_%M_%d_%m_%Y.txt'),"w")
head="LOS_status,Voltage_DDM,Temperature_DDM,RX1,RX2,RX3,RX4,BIAS1,BIAS2,BIAS3,BIAS4,TX1,TX2,TX3,TX4,Multimeter,TIMESTAMP" + '\n'
log.write(head)

pymsgbox.alert('Please check voltage level on Fluke Multimeter and Adjust it accordingly. Please set sweep on Kikusui PSU')

#Waveform generator output on

pymsgbox.alert('Set Properly Test Equipment')

now = time.strftime("%c")
print "Test Started at " + now

TE.start_counters()

for i in range (0,50): # minutes of test, test duration in minutes
	print "Minute n: "+str(i)+'\n'
	for k in range (1,60):
		poll=module.poller()
		volt_mm=mm.get_voltage()
		timestamp=time.strftime('%H_%M_%S')
		log.write(poll +',' +str(volt_mm)+ ',' + timestamp +'\n')
		time.sleep(0.94)
		
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

psu.close()
gen.close()

now = time.strftime("%c")
print "Test Finished at " + now









