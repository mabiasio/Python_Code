import pymsgbox
from Modules.sfp28 import *
from Instruments.Fluke_8846A import *
from Instruments.KikusuiPBZ20 import *
from Instruments.Agilent33600A import *
from Instruments.DLI100G40G import *
import time
import os


#module=sfp28()
#psu = KikusuiPBZ20('10.58.241.170')
gen = Agilent33600A('10.58.241.171')
#TE=DLI100G40G('10.58.241.161','8090')
#mm=Fluke_8846A(12)

print gen.identification()

gen.set_wfm(2, 'SIN')
gen.set_amplitude(2,'0.25')
gen.set_sweep_parameters(2,'100000','10000000','100')
gen.set_sweep_on(2)


