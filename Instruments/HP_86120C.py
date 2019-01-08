import time
import telnetlib
import os
import visa

class HP_86120C:
    def __init__(self, GPIB):
        try:
            self.GPIB = GPIB
            self.rm = visa.ResourceManager()
            self.multimeter = self.rm.open_resource('GPIB0::'+str(self.GPIB)+'::INSTR')
            self.multimeter.write(':INIT:CONT OFF')
            self.multimeter.write(':INIT:IMM')
        except:
            print "GPIB communication opening issue."

    def identification(self):
        # this function returns a string with Instrument name and HW details
        try:
            print self.multimeter.query('*IDN?')
        except:
            print "GPIB connection error"

    def get_WL(self):
        # this function returns a string with Instrument name and HW details
        try:
            measure=self.multimeter.query(':MEAS:SCAL:POW:WAV?')
        except:
            print "GPIB connection error"
            return None
        else:
            return float(measure)

    def get_pwr(self):
        # this function returns a string with Instrument name and HW details
        try:
            measure=self.multimeter.query(':MEAS:SCAL:POW?')
        except:
            print "GPIB connection error"
            return None
        else:
            return float(measure)
