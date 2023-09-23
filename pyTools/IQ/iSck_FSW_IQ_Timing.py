""" Rohde & Schwarz Automation for demonstration use """
from iSocket import iSocket                     # Import socket module
import logging
import timeit
global Freq

def Get_IQ_Data_Bin():
    # import struct
    global FSW
    FSW.write('FORMAT:DATA REAL,32')
    FSW.write('TRAC:IQ:DATA:FORM IQP')
    FSW.write('TRAC:IQ:DATA:MEM?')
    rdStr = FSW.read()
    numBytes = int(chr(rdStr[1]))               # Number of Bytes
    IQBytes  = rdStr[(numBytes + 2):-1]         # Remove Header
    # print(rdStr[2:numBytes+2])
    # recLen    = int(rdStr[2:2 + numBytes])
    # IQAscii  = struct.unpack("<" + 'f' * int(recLen / 4), IQBytes)
    # print(IQAscii[0:10])
    FSW.write('Format:DATA ASCII')
    return IQBytes

def IQ_Capture(capTime, clock, Freq):
    FSW.write('*CLS')
    FSW.write(':INST:SEL "IQ Analyzer"')        # Select Analog Demod
    FSW.write(f':SENS:FREQ:CENT {Freq}')        # Center Frequency
    FSW.write(f':TRAC:IQ:SRAT {clock}')         # Sampling Rate
    FSW.write(f':SENS:SWE:TIME {capTime}')      # Capture time
    FSW.query(':INIT:IMM;*OPC?')
    recLen = FSW.queryInt('TRAC:IQ:RLEN?')
    # print(f'Number IQ Data: {recLen} ASCII:{recLen * 18}')

    tick = timeit.default_timer()
    IQ_data = Get_IQ_Data_Bin()
    testtime = timeit.default_timer() - tick
    FSW.write('FORMAT:DATA ASCII')

    rate = recLen * 8 / testtime / 1e6
    data = f'{Freq/1e9:9.2f},{clock/1e6:7.2f},{capTime*1000:7.2f},Bin SCPI,'\
        f'{recLen:8d},{recLen * 8:10d},{len(IQ_data):10d},'\
        f'{testtime*1000:11.3f},{rate:12.3f}'
    logging.info(data)
    print(data)

def main():
    global FSW

    logging.basicConfig(level=logging.INFO,
                        filename=__file__.split('.')[0] + '.log', filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    FSW = iSocket().open('192.168.58.109', 5025)
    FSW.s.settimeout(5)
    Freq        = 24e9
    sampleRate  = 122.88e6
    header = 'Freq[GHz],Fs[MHz],CapTime,Transfer,IQ Pairs,Bytes Calc,Bytes Read,TTime[msec],Rate[MB/sec]'
    logging.info(header)
    print(header)

    for i in [0.05, 0.05, 0.03, 0.01, 0.005, 0.003, 0.001, 0.0005, 0.0003, 0.0001]:
        IQ_Capture(i, sampleRate, Freq)

main()
