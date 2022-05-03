""" Rohde & Schwarz Automation for demonstration use """
from iSocket import iSocket                 # Import socket module
import timeit

def Get_IQ_Data_Bin():
    # import struct
    FSW.write('FORMAT:DATA REAL,32')
    FSW.write('TRAC:IQ:DATA:FORM IQP')
    FSW.write('TRAC:IQ:DATA:MEM?')
    rdStr = FSW.read()
    numBytes = int(chr(rdStr[1]))                           # Number of Bytes
    IQBytes  = rdStr[(numBytes + 2):-1]                     # Remove Header
    # numIQ    = int(rdStr[2:2 + numBytes])
    # IQAscii  = struct.unpack("<" + 'f' * int(numIQ / 4), IQBytes)
    # print(IQAscii[0:10])
    FSW.write('Format:DATA ASCII')
    return IQBytes


FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)
Freq        = 24e9
clock       = 122.88e6
captureTime = 0.0001

FSW.write('*CLS')
FSW.write(':INST:SEL "IQ Analyzer"')        # Select Analog Demod
FSW.write(f':SENS:FREQ:CENT {Freq}')        # Center Frequency
FSW.write(f':TRAC:IQ:SRAT {clock}')         # Sampling Rate
FSW.write(f':SENS:SWE:TIME {captureTime}')  # Capture time
FSW.query(':INIT:IMM;*OPC?')
numIQ = FSW.queryInt('TRAC:IQ:RLEN?')
print(f'Number IQ Data: {numIQ} ASCII:{numIQ * 18}')

tick = timeit.default_timer()
CSVd = Get_IQ_Data_Bin()
testtime = timeit.default_timer() - tick

print(f'Error   : {FSW.query(":SYST:ERR?")}')
# print(f'File    : {fileName}')
print(f'Clock   : {clock}')
print(f'Cap Time: {numIQ / clock * 1000} msec')
print(f'Transfer: Binary Transfer')
print(f'numIQ   : {numIQ} x8 --> {numIQ * 8} Bytes')
print(f'ThrougPt: {numIQ * 8}bytes / {testtime:.3f} Sec = {numIQ * 8 / testtime / 1e6:.3f} MB/sec')
