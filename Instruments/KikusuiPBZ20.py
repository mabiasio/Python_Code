import time
import telnetlib	
import os


class KikusuiPBZ20:
	def __init__(self,ipaddress):
		try:
			self.ipaddress=ipaddress
			self.connessione=telnetlib.Telnet(self.ipaddress,5025)
			#self.connessione.read_until('\n')
		except:	
			print "Telnet opening connection error."
			
	def identification (self):
		#this function returns a string with Instrument name and HW details
		try:	
			self.connessione.write('*IDN?\n')
			out=self.connessione.read_until('\n')
		except:
			print "Telnet connection error"
			return None
		else:
			return out
			
	def set_signal_source (self,mode):
		#this function sets source input mode INT,EXT,BOTH(ADD)
		try:	
			self.connessione.write('SOUR:FUNC:SOUR '+mode+'\n')
		except:
			print "Telnet connection error"
			return None
			
	def set_voltage (self,voltage_out):
		#this function sets output voltage x.xxx V format integer type
		try:	
			self.connessione.write('SOUR:VOLT:LEV '+str(voltage_out)+'\n')
		except:
			print "Telnet connection error"
			return None

	
	def output_on (self):
		try:	
			self.connessione.write('OUTP:STAT ON\n')
		except:
			print "Telnet connection error"
			return None
	
	def output_off (self):
		try:	
			self.connessione.write('OUTP:STAT OFF\n')		
		except:
			print "Telnet connection error"
			return None
			
	def ac_on (self):
		try:	
			self.connessione.write('SOUR:AC:STAT ON\n')		
		except:
			print "Telnet connection error"
			return None
			
	def ac_off (self):
		try:	
			self.connessione.write('SOUR:AC:STAT OFF\n')		
		except:
			print "Telnet connection error"
			return None		

	def set_ac_amplitude (self,amp):
		#amp = integer paramenter for ac ripple amplitude in x.xx V format
		try:
			self.connessione.write('SOUR:VOLT:AC:AMPL '+str(amp)+'\n')
		except:
			print "Telnet connection error"
			return None
			
	def set_ac_frequency (self,freq):
		#amp = integer paramenter for ac ripple frequency in xxxxxx.xx Hz format
		try:
			self.connessione.write('SOUR:FREQ '+str(freq)+'\n')
		except:
			print "Telnet connection error"
			return None

	def close (self):
		try:
			self.connessione.close()
		except:
			print "Telnet closing connection error."
			
