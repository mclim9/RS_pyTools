"""R&S Example code"""
from iVISA import iVISA
import timeit

instr   = iVISA().open('192.168.58.109')

# instr.write('FORM:DATA ASCII')
# rdStr = float(instr.query(f':FETC:CC1:SUMM:EVM:ALL?'))

tick = timeit.default_timer()
rdStr = instr.query('*IDN?')
TotTime = timeit.default_timer() - tick
print(f'{TotTime*1000:.3f}mSec,{rdStr}')
