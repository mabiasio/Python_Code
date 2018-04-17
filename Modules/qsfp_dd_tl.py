import time
import math
import string
from Aardvark.aardvark_py import *
from array import array

class qsfp_dd_tl:
    def __init__(self):
        self.addr = 0x50
        self.handle = aa_open(0)
        self.i2c_counter = 0
        if (self.handle <= 0):
            print "Unable to open Aardvark device on port 0"
            print "Error code = %d" % handle
            sys.exit()
        # Ensure that the I2C subsystem is enabled
        aa_configure(self.handle, AA_CONFIG_SPI_I2C)
        # Pull up resitors already present in the MCB
        aa_i2c_pullup(self.handle, AA_I2C_PULLUP_NONE)
        # I2C Master configuration
        aa_i2c_slave_disable(self.handle)
        # No Power supply provided by Aardwark module
        aa_target_power(self.handle, AA_TARGET_POWER_NONE)
        # I2C Bitrate
        aa_i2c_bitrate(self.handle, 100)

    def get_i2c_counter(self):
        return self.i2c_counter
		
    def get_serial_number(self):
        time.sleep(0.04)
        data_out = array('B', [127,0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out) #Set upper page to 0
        if (res < len(data_out)):
            print "I2C write error. Written bytes = "+ str(res)+"\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [196])
        data_in = array('B', [0 for i in range(16)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        SN=''
        for item in data_in:
            SN = SN + chr(item)
        return SN

    def get_cutoff(self):
        time.sleep(0.04)
        data_out = array('B', [127,2])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out) #Set upper page to 0
        if (res < len(data_out)):
            print "I2C write error. Written bytes = "+ str(res)+"\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [134])
        data_in = array('B', [0 for i in range(1)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print " Cut_off temperature set " + str(data_in[0]) +" deg C"

    def set_cutoff(self, c_o):
        time.sleep(0.04)
        data_out = array('B', [127,2])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out) #Set upper page to 0
        if (res < len(data_out)):
            print "I2C write error. Written bytes = "+ str(res)+"\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [134,int(c_o)])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print " Cut_off temperature set " + str(c_o) +" deg C"

    def get_vendor_name(self):
        time.sleep(0.04)
        data_out = array('B', [127, 0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 0
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [148])
        data_in = array('B', [0 for i in range(16)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        VN = ''
        for item in data_in:
            VN = VN + chr(item)
        return VN

    def get_voltage(self):
        time.sleep(0.04)
        data_out = array('B', [26])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        res = hex(data_in[0])+str(hex(data_in[1])[2:]).zfill(2) #forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        tmp =int(res,0)
        return (tmp * 6.55)/65535

    def get_temperature(self):
        time.sleep(0.04)
        data_out = array('B', [22])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        string = hex(data_in[0])+str(hex(data_in[1])[2:]).zfill(2) #forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        res=int(string,0)
        if res > 0x7fff:
            res -= 65536
        temp_1 = (res * 1.0)/256
        time.sleep(0.04)
        data_out = array('B', [24])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        string = hex(data_in[0])+str(hex(data_in[1])[2:]).zfill(2) #forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        res=int(string,0)
        if res > 0x7fff:
            res -= 65536
        temp_2 = (res * 1.0)/256
        time.sleep(0.04)
        data_out = array('B', [30])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        string = hex(data_in[0])+str(hex(data_in[1])[2:]).zfill(2) #forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        res=int(string,0)
        if res > 0x7fff:
            res -= 65536
        temp_3 = (res * 1.0)/256
        time.sleep(0.04)
        data_out = array('B', [32])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        string = hex(data_in[0])+str(hex(data_in[1])[2:]).zfill(2) #forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        res=int(string,0)
        if res > 0x7fff:
            res -= 65536
        temp_4 = (res * 1.0)/256
        return [temp_1,temp_2,temp_3,temp_4]

    def set_dissipation_off(self):
        time.sleep(0.04)
        data_out = array('B', [127, 2]) #page 2
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 3
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [82,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [83,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [84,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [85,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [86,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [87,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [88,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [89,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "Power dissipation turned OFF"

    def set_dissipation_5(self):
        time.sleep(0.04)
        data_out = array('B', [127, 2]) #page 2
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 3
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [129,0x0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [83,0x08])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [84,0x08])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [88,0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "Power dissipation set at 5 W"

    def set_dissipation_7(self):
        time.sleep(0.04)
        data_out = array('B', [127, 2]) #page 2
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 3
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [129, 0x0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [82,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [83,0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [84,0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [85,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [86,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [87,0x04])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [88,0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [89,0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "Power dissipation set at 7 W"

    def set_dissipation_9(self):
        time.sleep(0.04)
        data_out = array('B', [127, 2]) #page 2
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 3
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [129, 0x0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [82,0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [83,0x08])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [84,0x08])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [85,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [86,0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [87,0x04])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [88,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [89,0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "Power dissipation set at 9 W"

    def set_dissipation_11(self):
        time.sleep(0.04)
        data_out = array('B', [127, 2])  # page 2
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 3
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [129, 0x0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [135, 0x01])  #Power override disabled
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [82, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [83, 0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [84, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [85, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [86, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [87, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [88, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [89, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "Power dissipation set at 11 W"

    def set_dissipation_13(self):
        time.sleep(0.04)
        data_out = array('B', [127, 2])  # page 2
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 3
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [129, 0x0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [135, 0x01])  #Power override disabled
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [82, 0x04])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [83, 0x04])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [84, 0x10])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [85, 0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [86, 0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [87, 0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [88, 0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [89, 0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "Power dissipation set at 13 W"

    def set_dissipation_15(self):
        time.sleep(0.04)
        data_out = array('B', [127, 2])  # page 2
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)  # Set upper page to 3
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [129, 0x0])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [135, 0x01])  #Power override disabled
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [82, 0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [83, 0x08])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [84, 0x0C])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [85, 0x02])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [86, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [87, 0x00])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [88, 0x03])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [89, 0x01])
        res = aa_i2c_write(self.handle, self.addr, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "Power dissipation set at 15 W"
