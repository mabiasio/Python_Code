import time
import math
from Aardvark.aardvark_py import *
from array import array

class sfp28:
    def __init__(self):
        self.addr_low = 0x50
        self.addr_high = 0x51
        self.handle = aa_open(0)
        self.i2c_counter = 0
        if (self.handle <= 0):
            print "Unable to open Aardvark device on port 0"
            print "Error code = %d" % str(self.handle)
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
        data_out = array('B', [68])
        data_in = array('B', [0 for i in range(16)])
        res = aa_i2c_write_read(self.handle, self.addr_low, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        SN = ''
        for item in data_in:
            SN = SN + chr(item)
        return SN

    def get_vendor_PN(self):
        data_out = array('B', [40])
        data_in = array('B', [0 for i in range(16)])
        res = aa_i2c_write_read(self.handle, self.addr_low, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        PN = ''
        for item in data_in:
            PN = PN + chr(item)
        return PN

    def get_vendor_name(self):
        time.sleep(0.04)
        data_out = array('B', [20])
        data_in = array('B', [0 for i in range(16)])
        res = aa_i2c_write_read(self.handle, self.addr_low, AA_I2C_NO_FLAGS, data_out, data_in)
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
        data_out = array('B', [98])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        res = hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(2)  # forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        tmp = int(res, 0)
        return (tmp * 6.55) / 65535

    def mode_25G(self):
        time.sleep(0.04)
        data_out = array('B', [120])
        data_in = array('B', [0 for i in range(1)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [120, int((int(hex(data_in[0])[2:],16) | 0b00001110))])
        res = aa_i2c_write(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [114])
        data_in = array('B', [0 for i in range(1)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        time.sleep(0.04)
        data_out = array('B', [114, int((int(hex(data_in[0])[2:], 16) | 0x03))])
        res = aa_i2c_write(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out)
        if (res < len(data_out)):
            print "I2C write error. Written bytes = " + str(res) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        print "25G Mode, CDR ON, CTLE Fixed 3 dB"

    def get_temperature(self):
        time.sleep(0.04)
        data_out = array('B', [96])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        string = hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(2)  # forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        res = int(string, 0)
        if res > 0x7fff:
            res -= 65536
        return (res * 1.0) / 256

    def get_RX_power(self):  # output value is in dBm
        time.sleep(0.04)
        data_out = array('B', [104])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        lane1 = 10 * math.log10((int((hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(2)), 16) + 1) / 10000.0)
        return [lane1]

    def get_TX_power(self):
        time.sleep(0.04)
        data_out = array('B', [102])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        lane1 = 10 * math.log10((int((hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(2)), 16) + 1) / 10000.0)
        return [lane1]

    def poller(self):
        # Byte 3 reading
        data_out = array('B', [110])
        data_in = array('B', [0 for i in range(1)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        status = hex(data_in[0])
        # Temp Reading
        data_out = array('B', [96])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        string = hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(
            2)  # forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        res = int(string, 0)
        if res > 0x7fff:
            res -= 65536
        temperature = (res * 1.0) / 256
        # Voltage Reading
        data_out = array('B', [98])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        res = hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(
            2)  # forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        tmp = int(res, 0)
        voltage = (tmp * 6.55) / 65535
        # Rx_Power_1_Reading
        data_out = array('B', [104])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        RX_1 = 10 * math.log10((int((hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(2)), 16) + 1) / 10000.0)
        # Tx_Bias_1
        data_out = array('B', [100])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        res = hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(
            2)  # forma 0x yy zz. If zz is composed by only one HEX value, zfill function will insert 0 on top of zz nibble
        tmp = int(res, 0)
        BIAS_1 = (tmp * 131.0) / 65535
        # Tx_Power_1_Reading
        data_out = array('B', [102])
        data_in = array('B', [0 for i in range(2)])
        res = aa_i2c_write_read(self.handle, self.addr_high, AA_I2C_NO_FLAGS, data_out, data_in)
        if (res[0] == 1) or (res[0] == 3) or (res[0] == 4) or (res[0] == 5) or (res[0] == 6):
            print "I2C read error. Error return code = " + str(res[0]) + "\n"
            self.i2c_counter = self.i2c_counter + 1
            return "None"
        TX_1 = 10 * math.log10((int((hex(data_in[0]) + str(hex(data_in[1])[2:]).zfill(2)), 16) + 1) / 10000.0)
        result_string = str(status) + ',' + str(voltage) + ',' + str(temperature) + ',' + str(RX_1) + ',' + str(BIAS_1)  + ',' + str(TX_1)
        return result_string


