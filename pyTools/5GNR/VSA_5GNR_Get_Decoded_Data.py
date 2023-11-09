import socket

def sQuery(SCPI):                                       # Socket Query
    sWrite(SCPI)
    sOut = FSW.recv(10000000).decode().strip()
    return sOut

def sWrite(SCPI):                                       # Socket Write
    FSW.sendall(f'{SCPI}\n'.encode())

FSW = socket.socket()
FSW.connect(('192.168.58.109', 5025))
FSW.settimeout(5)

sWrite(':SENS:NR5G:DEM:DDAT BDES')                      # Data type: BDES | ADES | DPD
sWrite(':LAY:REPL:WIND "4",BSTR')                       # Replace Window 4 w/ Bitstream
sWrite(':INIT:CONT OFF')                                # Single Sweep

data1 = sQuery(':TRAC4:DATA? TRACE1')
data2 = sQuery(':TRAC4:DATA? TRACE2')
data3 = sQuery(':TRAC4:DATA? TRACE3')
data4 = sQuery(':TRAC4:DATA? TRACE4')
totalData = (data1 + data2 + data3 + data4).split(',')  # Concatenate Data
# BWP; SubFrame; Slot; AllocID; Codeword1; Modulation; #decoded bits; #bit Error; #symbol/bit; Bitstream
segStart = 0
numBitsOffset = 8

fily = open(__file__.split('.')[0] + '.txt', '+a')
for i in range(10):
    numBits   = int(totalData[segStart + numBitsOffset])
    bitsStart = segStart + numBitsOffset + 1
    bitsStop  = segStart + numBitsOffset + numBits
    bits      = ''.join(totalData[bitsStart:bitsStop])
    outString = f'{totalData[segStart]},{totalData[segStart + 1]},{totalData[segStart + 2]},{numBits},{bits}'
    print(outString)
    fily.write(outString)                               # Write to file

    segStart = bitsStop + 1

pass
