import time
import telnetlib	

class Agilent33600A:
	def __init__(self,ipaddress):
		try:
			self.ipaddress=ipaddress
			self.connessione=telnetlib.Telnet(self.ipaddress,5024)
			self.connessione.read_until('33600A>')
		except:	
			print "Telnet opening connection error."
			
	def identification (self):
		#this function returns a string with Instrument name and HW details
		try:	
			self.connessione.write('*IDN?\n')
			out=self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None
		else:
			return out[:(len(out)-9)]
			
	
	def output_on (self,channel):
		#channel = integer parameter for channel selection
		try:	
			self.connessione.write('OUTP'+str(channel)+' ON\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None
	
	def output_off (self,channel):
		#channel = integer parameter for channel selection
		try:	
			self.connessione.write('OUTP'+str(channel)+' OFF\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None
			
	def set_wfm (self,channel,wfm):
		#channel = integer parameter for channel selection
		#wfm = string paramenter for wfm type selection (SIN,SQU,RAMP,PULS,TRI,PRBS,NOIS,ARB)
		try:	
			self.connessione.write('SOUR'+str(channel)+':FUNC '+wfm+'\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None
			
	def set_frequency (self,channel,freq):
		#channel = integer parameter for channel selection
		#freq = string paramenter for frequency selection in Hertz (+X.XE+0Y format)
		try:
			self.connessione.write('SOUR'+str(channel)+':FREQ '+freq+'\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_noise_bw (self,channel,bandwidth):
		#channel = integer parameter for channel selection
		#freq = string paramenter for frequency selection in Hertz (+X.XE+0Y format)
		try:
			self.connessione.write('SOUR'+str(channel)+':FUNC:NOIS:BAND '+bandwidth+'\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None
			
	def set_amplitude (self,channel,amp):
		#channel = integer parameter for channel selection
		#amp = string paramenter for amplitude selection in Volt pp (+X.XE+0Y format)
		try:
			self.connessione.write('SOUR'+str(channel)+':VOLT:UNIT VPP\n')
			self.connessione.read_until('33600A>')
			self.connessione.write('SOUR'+str(channel)+':VOLT '+amp+'\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_offset (self,channel,offset):
		#channel = integer parameter for channel selection
		#offset = string paramenter for offset selection in Volt pp (+X.XE+0Y format)
		try:
			self.connessione.write('SOUR'+str(channel)+':VOLT:OFFS '+offset+'\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_hi_z (self,channel):
		#channel = integer parameter for channel selection
		#offset = string paramenter for offset selection in Volt pp (+X.XE+0Y format)
		try:
			self.connessione.write('OUTP'+str(channel)+':LOAD INF'+'\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None
			
	def close (self):
		try:
			self.connessione.close()
		except:
			print "Telnet closing connection error."
			
