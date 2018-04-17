import time
import telnetlib



class DLI100G40G:
	def __init__(self, ipaddress, port):
		self.ipaddress = ipaddress
		self.port = port
		try:
			self.connessione = telnetlib.Telnet(self.ipaddress, self.port)
			self.connessione.write('LOGIN Admin Admin1\n')
			self.connessione.read_until('\n',5)
			self.connessione.write('*IDN?\n')
			IDN=self.connessione.read_until('\n',5)
			print "Connected with "+IDN[0:(len(IDN)-2)]+" traffic generator"
			self.connessione.write('INST:MPM100PACKET\n')
			IDN=self.connessione.read_until('\n',5)
			self.connessione.write('INST?\n')
			IDN=self.connessione.read_until('\n',5)
			print IDN
		except:
			print "Connection with DLI100G40G "+self.ipaddress+" unavailable. Please check ETH connection\n"
			
	def logout(self):
		try:
			self.connessione.write('INST:NONE\n')
			R=self.connessione.read_until('\n',5)
			self.connessione.write('LOGOUT\n')
			R=self.connessione.read_until('\n',5)
		except:
			print "Connection with DLI100G40G "+self.ipaddress+" unavailable. Please check ETH connection\n"
			
	def start_counters(self):
		try:
			self.connessione.write('INIT\n')
			R=self.connessione.read_until('\n',5)
			print R
		except:
			print "Connection with DLI100G40G "+self.ipaddress+" unavailable. Please check ETH connection\n"
			
	def stop_counters(self):
		try:
			self.connessione.write('ABOR\n')
			R=self.connessione.read_until('\n',5)
			print R
		except:
			print "Connection with DLI100G40G "+self.ipaddress+" unavailable. Please check ETH connection\n"


	def get_alarms(self):
		try:
			self.connessione.write('RES:SCANALARMS?\n')
			alarms=self.connessione.read_until('\n',5)
		except:
			print "Connection with DLI100G40G "+self.ipaddress+" unavailable. Please check ETH connection\n"
		else:
			if alarms[0:2]=='+0':
				return None
			else:
				return alarms

	def get_events(self):
		try:
			self.connessione.write('RES:EVENTLOG 1?\n')
			events=self.connessione.read_until('\n',5)
		except:
			print "Connection with DLI100G40G "+self.ipaddress+" unavailable. Please check ETH connection\n"
		else:
			res_list=events.split(';')
			for i in range (0,len(res_list)):
				print res_list[i]



	def get_results(self):
		try:
			self.connessione.write('RES:RXPACK?\n')
			RX_packets=self.connessione.read_until('\n',5)
			self.connessione.write('RES:TXPACK?\n')
			TX_packets=self.connessione.read_until('\n',5)
			self.connessione.write('RES:RXPACK:BYT?\n')
			RX_bytes=self.connessione.read_until('\n',5)
			self.connessione.write('RES:TXBYT?\n')
			TX_bytes=self.connessione.read_until('\n',5)
		except:
			print "Connection with DLI100G40G "+self.ipaddress+" unavailable. Please check ETH connection\n" 
			
		else:
			return TX_packets[0:(len(TX_packets)-2)]+','+RX_packets[0:(len(RX_packets)-2)]+','+TX_bytes[0:(len(TX_bytes)-2)]+','+RX_bytes[0:(len(RX_bytes)-2)]

#TE = DLI100G40G('10.58.232.72','8090')
#time.sleep(1)
#TE.start_counters()
#time.sleep(5)
#TE.stop_counters()
#TE.get_events()
#ciccio=TE.get_results()
#print ciccio
#TE.logout()



