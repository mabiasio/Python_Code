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
			self.connessione.write('SOUR'+str(channel)+':FUNC:NOIS:BWID '+bandwidth+'\n')
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

	def set_am_modulation (self,channel,format):
		#channel = integer parameter for channel selection
		# format = string paramenter for wfm type selection (SIN,SQU,RAMP,PULS,TRI,PRBS,NOIS,ARB)
		try:
			self.connessione.write('SOUR'+str(channel)+':AM:INT:FUNC '+ format + '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_am_frequency (self,channel,frequency):
		#channel = integer parameter for channel selection
		# freq = string paramenter for frequency selection in Hertz (+X.XE+0Y format)
		try:
			self.connessione.write('SOUR'+str(channel)+':AM:INT:FREQ '+ frequency + '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_am_depth (self,channel,dpt):
		#channel = integer parameter for channel selection
		# dpt = string paramenter for modulation depth (+X.XE+0Y format)
		try:
			self.connessione.write('SOUR'+str(channel)+':AM:DEPT '+ dpt + '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_am_modulation_on (self,channel):
		#channel = integer parameter for channel selection
		try:
			self.connessione.write('SOUR'+str(channel)+':AM:STAT 1'+ '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_sweep_on (self,channel):
		#channel = integer parameter for channel selection
		try:
			self.connessione.write('SOUR'+str(channel)+':SWE:STAT 1'+ '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_am_modulation_off (self,channel):
		#channel = integer parameter for channel selection
		try:
			self.connessione.write('SOUR'+str(channel)+':AM:STAT 0'+ '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_sweep_off (self,channel):
		#channel = integer parameter for channel selection
		try:
			self.connessione.write('SOUR'+str(channel)+':SWE:STAT 0'+ '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None

	def set_sweep_parameters (self,channel,start,stop,time):
		# channel = integer parameter for channel selection
		# start = string parameter for start frequency
		# stop = string parameter for stop frequency
		# time = string pamater for sweeping time in seconds
		try:
			self.connessione.write('SOUR'+str(channel)+':FREQ:STAR '+ start + '\n')
			self.connessione.read_until('33600A>')
			self.connessione.write('SOUR' + str(channel) + ':FREQ:STOP ' + stop + '\n')
			self.connessione.read_until('33600A>')
			self.connessione.write('SOUR' + str(channel) + ':SWE:TIME ' + time + '\n')
			self.connessione.read_until('33600A>')
		except:
			print "Telnet connection error"
			return None
			
	def close (self):
		try:
			self.connessione.close()
		except:
			print "Telnet closing connection error."
			
