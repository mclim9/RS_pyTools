"""R&S Example code"""
from iVISA import iVISA

# #############################################################################
# ## Code Begin
# #############################################################################
instr   = iVISA().open('192.168.58.109')

# instr.write('FORM:DATA ASCII')
# rdStr = float(instr.query(f':FETC:CC1:SUMM:EVM:ALL?'))
print(instr.query('*IDN?'))
