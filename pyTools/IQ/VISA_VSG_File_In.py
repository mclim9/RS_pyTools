"""R&S Example code"""
from iVISA import iVISA

# Read Source Waveform
wvName  = 'test.wv'
f       = open(wvName, 'rb')
byteAry = f.read()
f.close()

instr   = iVISA().open('192.168.58.114')
numByte = len(byteAry)                          # Bytes in file
numHead = len(str(numByte))                     # Length of numByte
SCPI    = f'MMEM:DATA "/var/user/{wvName}",#{numHead}{numByte}'
command = bytes(SCPI, 'utf-8') + byteAry

instr.VISA.write_raw(command)
print(instr.query('SYST:ERR?'))
