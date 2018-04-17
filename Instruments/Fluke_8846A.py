import time
import telnetlib
import os
import visa

class Fluke_8846A:
    def __init__(self, GPIB):
        try:
            self.GPIB = GPIB
            self.rm = visa.ResourceManager()
            self.multimeter = self.rm.open_resource('GPIB0::'+str(self.GPIB)+'::INSTR')
        except:
            print "GPIB communication opening issue."

    def identification(self):
        # this function returns a string with Instrument name and HW details
        try:
            print self.multimeter.query('*IDN?')
        except:
            print "GPIB connection error"

    def get_voltage(self):
        # this function returns a string with Instrument name and HW details
        try:
            measure=self.multimeter.query('VAL1?')
        except:
            print "GPIB connection error"
            return None
        else:
            return float(measure)
