"""R&S Example code"""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Code Begin
# #############################################################################
fileName = 'test.wv'

K2      = iSocket().open('192.168.58.114',5025)
f = open(fileName, 'rb')
data    = f.read()
f.close()

# data = b'hello'
numBytes = len(data)
numHead  = len(str(numBytes))
SCPI     = f'MMEMory:DATA "/var/user/{fileName}",#{numHead}{numBytes}'
command  = bytes(SCPI, 'utf-8') + data
K2.write(SCPI)
