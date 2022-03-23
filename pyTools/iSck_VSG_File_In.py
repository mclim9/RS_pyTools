"""R&S Example code"""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Code Begin
# #############################################################################
fileName = 'iSck_VSG_File_In.wv'

K2      = iSocket().open('192.168.58.114', 5025)
f = open(fileName, 'rb')
data    = f.read()
f.close()

# data = b'hello'
numBytes = len(data)
numHead  = len(str(numBytes))
SCPI     = f'MMEM:DATA "/var/user/{fileName}",#{numHead}{numBytes}'
command  = bytes(SCPI, 'utf-8') + data
K2.writeBin(command)
asdf = K2.query(':SYST:ERR?')
