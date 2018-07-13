from SUB20.mdio import *
import time
import math

 #Execute a mdio cluase 45 transaction.
 #Returnes an integer on read or read post increment.
 #op_code
 #0 is for Address
 #1 is for Write
 #2 is for Read
 #3 is for Read post increment


class cfp2:

    def __init__(self):
        self.PHY_address = 1
        self.port_address = 1


    def single_read (self, mem_addr):
        transaction(0,self.PHY_address,self.port_address,mem_addr)
        data = transaction(2,self.PHY_address,self.port_address,mem_addr)
        return data

    def get_temperature(self):
        transaction(0, self.PHY_address, self.port_address, 0xA02F)
        data = transaction(2, self.PHY_address, self.port_address, 0xA02F)
        if data > 0x7fff:
            data -= 65536
        return (data * 1.0)/256

    def get_voltage(self):
        transaction(0, self.PHY_address, self.port_address, 0xA030)
        data = transaction(2, self.PHY_address, self.port_address, 0xA030)
        return (data / 10000.0)

    def get_SN(self):
        SN_RAW=[]
        for i in range (0,15):
            transaction(0, self.PHY_address, self.port_address, 0x8044+i)
            SN_RAW.append(transaction(2, self.PHY_address, self.port_address, 0x8044+i))
        print SN_RAW
        SN=''
        for item in SN_RAW:
            SN = SN + chr(item)
        return SN

    def get_vendor_PN(self):
        PN_RAW=[]
        for i in range (0,15):
            transaction(0, self.PHY_address, self.port_address, 0x8034+i)
            PN_RAW.append(transaction(2, self.PHY_address, self.port_address, 0x8034+i))
        print PN_RAW
        PN=''
        for item in PN_RAW:
            PN = PN + chr(item)
        return PN


    def get_vendor_name(self):
        SN_RAW=[]
        for i in range (0,15):
            transaction(0, self.PHY_address, self.port_address, 0x8021+i)
            SN_RAW.append(transaction(2, self.PHY_address, self.port_address, 0x8021+i))
        print SN_RAW
        SN=''
        for item in SN_RAW:
            SN = SN + chr(item)
        return SN

    def set_OTU_rate(self):
        transaction(0, self.PHY_address, self.port_address, 0xA011)
        data=transaction(3, self.PHY_address, self.port_address, 0x0)

        transaction(0, self.PHY_address, self.port_address, 0xA011)
        transaction(1, self.PHY_address, self.port_address, (data | 0x0006))


        transaction(0, self.PHY_address, self.port_address, 0xA012)
        data=transaction(3, self.PHY_address, self.port_address, 0x0)

        transaction(0, self.PHY_address, self.port_address, 0xA012)
        transaction(1, self.PHY_address, self.port_address, (data | 0x0006))

    def set_IEEE_rate(self):
        transaction(0, self.PHY_address, self.port_address, 0xA011)
        data=transaction(3, self.PHY_address, self.port_address, 0x0)

        transaction(0, self.PHY_address, self.port_address, 0xA011)
        transaction(1, self.PHY_address, self.port_address, (data & 0xFFF9))


        transaction(0, self.PHY_address, self.port_address, 0xA012)
        data=transaction(3, self.PHY_address, self.port_address, 0x0)

        transaction(0, self.PHY_address, self.port_address, 0xA012)
        transaction(1, self.PHY_address, self.port_address, (data & 0xFFF9))

    def get_ctle(self):

        transaction(0, self.PHY_address, self.port_address, 0xA440)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_1 = str(bin(data))[2:].zfill(16)
        ctle_1 = int(lane_1[1:8],2)
        transaction(0, self.PHY_address, self.port_address, 0xA441)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_2 = str(bin(data))[2:].zfill(16)
        ctle_2 = int(lane_2[1:8],2)
        transaction(0, self.PHY_address, self.port_address, 0xA442)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_3 = str(bin(data))[2:].zfill(16)
        ctle_3 = int(lane_3[1:8],2)
        transaction(0, self.PHY_address, self.port_address, 0xA443)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_4 = str(bin(data))[2:].zfill(16)
        ctle_4 = int(lane_4[1:8],2)
        return [ctle_1,ctle_2,ctle_3,ctle_4]

    def set_ctle(self,a,b,c,d):
        #CTLE has 19 steps
        transaction(0, self.PHY_address, self.port_address, 0xA440)
        transaction(1, self.PHY_address, self.port_address, (0x8000+(int(hex(a),16)*0x100)))
        transaction(0, self.PHY_address, self.port_address, 0xA441)
        transaction(1, self.PHY_address, self.port_address, (0x8000+(int(hex(b),16)*0x100)))
        transaction(0, self.PHY_address, self.port_address, 0xA442)
        transaction(1, self.PHY_address, self.port_address, (0x8000+(int(hex(c),16)*0x100)))
        transaction(0, self.PHY_address, self.port_address, 0xA443)
        transaction(1, self.PHY_address, self.port_address, (0x8000+(int(hex(d),16)*0x100)))

    def get_RX_power(self):
        transaction(0, self.PHY_address, self.port_address, 0xA2D0)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_1 = 10 * math.log10(data / 10000.0)
        transaction(0, self.PHY_address, self.port_address, 0xA2D1)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_2 = 10 * math.log10(data / 10000.0)
        transaction(0, self.PHY_address, self.port_address, 0xA2D2)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_3 = 10 * math.log10(data / 10000.0)
        transaction(0, self.PHY_address, self.port_address, 0xA2D3)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_4 = 10 * math.log10(data / 10000.0)
        return [lane_1,lane_2,lane_3,lane_4]

    def get_TX_power(self):
        transaction(0, self.PHY_address, self.port_address, 0xA2B0)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_1 = 10 * math.log10(data / 10000.0)
        transaction(0, self.PHY_address, self.port_address, 0xA2B1)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_2 = 10 * math.log10(data / 10000.0)
        transaction(0, self.PHY_address, self.port_address, 0xA2B2)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_3 = 10 * math.log10(data / 10000.0)
        transaction(0, self.PHY_address, self.port_address, 0xA2B3)
        data = transaction(3, self.PHY_address, self.port_address, 0x0)
        lane_4 = 10 * math.log10(data / 10000.0)
        return [lane_1,lane_2,lane_3,lane_4]











