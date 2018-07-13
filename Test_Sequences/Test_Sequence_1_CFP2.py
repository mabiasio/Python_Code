import pymsgbox
from Modules.CFP2 import *
from Instruments.Fluke_8846A import *
from Instruments.KikusuiPBZ20 import *
from Instruments.Agilent33600A import *
from Instruments.DLI100G40G import *
import time
import os

module=cfp2()
psu=KikusuiPBZ20('10.58.241.170')
gen=Agilent33600A('10.58.241.171')
TE=DLI100G40G('10.58.241.161','8090')
mm=Fluke_8846A(12)

#print PSU and Wafeform Generator IDs

psu.identification()
gen.identification()


gen.output_off(1)
gen.set_wfm(1,'TRI')
gen.set_frequency(1,'23E-06') # 23 uHZ
gen.set_amplitude(1,'3.5E-1') #340 mVPP



#PSU settings 3,3 VDC + external signal
psu.set_signal_source('BOTH')
psu.set_voltage('3.410')
psu.output_on()
time.sleep(1)


#module configuration
M_SN=module.get_SN()
M_VN=module.get_vendor_name()

print 'Module under test id: ' + M_VN + ' ' + M_SN + '\n'

#Pseudo-initialization sequence
module.set_ctle(10,10,10,10)

log=open("Test_1_CFP2_"+ M_VN + '_' + M_SN + time.strftime('%H_%M_%d_%m_%Y.txt'),"w")
head="Voltage_DDM,Temperature_DDM,TX1,TX2,TX3,TX4,RX1,RX2,RX3,RX4,TIMESTAMP" + '\n'
log.write(head)

pymsgbox.alert('Please check voltage level on Fluke Multimeter and Adjust it accordingly')

#Waveform generator output on
gen.output_on(1)

pymsgbox.alert('Set Properly Test Equipment')

now = time.strftime("%c")
print "Test Started at " + now

TE.start_counters()

for i in range (0,750): # minutes of test, test duration in minutes
	print "Minute n: "+str(i)+'\n'
	for k in range (1,60):
		tx_pwr=module.get_TX_power()
		rx_pwr=module.get_RX_power()
		volt=module.get_voltage()
		temp=module.get_temperature()
		timestamp=time.strftime('%H_%M_%S')
		log.write(str(volt) +','+str(temp) +','+str(tx_pwr[0])+','+str(tx_pwr[1])+','+str(tx_pwr[2])+','+str(tx_pwr[3])+','+str(rx_pwr[0])+','+str(rx_pwr[1])+','+str(rx_pwr[2])+','+str(rx_pwr[3])+',' + timestamp +'\n')
		time.sleep(0.9)
		
TE.stop_counters()
traffic_res=TE.get_results()
print "Alarms on DLI Test Set"
print TE.get_alarms()
print "Events on DLI Test Set"
TE.get_events()
TE.logout()
log.close()
#psu.output_off()
gen.output_off(1)
psu.close()
gen.close()

now = time.strftime("%c")
print "Test Finished at " + now









