"""R&S Example code"""
from iVISA import iVISA

# #############################################################################
# ## Code Begin
# #############################################################################
fileName = 'CW__I_m0_25__Q_0.wv'
fileName = 'EHT320SMUGILTF16.0usMCS5.wv'

K2       = iVISA().open('192.168.58.114')
K2.write(f'MMEMory:DATA? "/var/user/{fileName}"')
rdStr    = K2.read()

numBytes = int(chr(rdStr[1]))                           # Number of Bytes
numIQ    = int(rdStr[2:2 + numBytes])
data     = rdStr[(numBytes + 2):-1]                     # Remove Header

f = open(fileName,'wb')
f.write(data)
f.close()
