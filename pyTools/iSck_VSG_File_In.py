from iSocket import iSocket                 # Import socket module
import timeit

def findData(data, string):
    strLen = len(string)
    dstart = data.find(string)
    begStr = data[dstart + strLen:dstart + 20]
    cutStr = begStr[:begStr.find(b'}')]
    return cutStr.decode()

# #############################################################################
# ## Code Begin
# #############################################################################
fileName = 'iSck_VSG_File_In-NR-FR1-TM1_1.wv'
f = open(fileName, 'rb')
data    = f.read()
f.close()

numBytes = len(data)
numHead  = len(str(numBytes))

K2       = iSocket().open('192.168.58.115', 5025)
SCPI     = f'MMEM:DATA "/var/user/{fileName}",#{numHead}{numBytes}'
command  = bytes(SCPI, 'utf-8') + data
tick = timeit.default_timer()
K2.writeBin(command)
testtime = timeit.default_timer() - tick

samples  = int(findData(data, b'SAMPLES:'))
clock    = int(findData(data, b'CLOCK:'))
print(f'Error   : {K2.query(":SYST:ERR?")}')
print(f'File    : {fileName}')
print(f'Samples : {samples}')
print(f'Clock   : {clock}')
print(f'Duration: {samples / clock * 1000} msec')
print(f'Transfer: Binary Transfer')
print(f'')
print(f'NumBytes: {numBytes}')
print(f'Time    : {testtime:.3f} Sec')
print(f'Thrput  : {numBytes/testtime/1e6:.3f} MB /sec')
