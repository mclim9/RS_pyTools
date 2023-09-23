from iSocket import iSocket                 # Import socket module
import numpy as np
import timeit

def readFile():
    f = open('iSck_VSG_IQ_Timing.env', 'r')
    data    = f.readlines()
    f.close()
    IData = []
    QData = []
    for line in data:
        if line[0] != '#':
            IQ = line.strip().split(',')
            IData.append(float(IQ[0]))
            QData.append(float(IQ[1]))
    return IData, QData

def IQ_Write(IData, QData, clock):
    # ## ASCII
    scpi  = f':MMEM:DATA:UNPR "NVWFM://var//user//{fileName}.wv",#' # Ascii Cmd
    numBytes = str(len(IData) * 4)                                  # Calc IQ bytes
    scpi  = scpi + str(len(numBytes)) + numBytes                    # Calc iqsize length str
    # ## Binary
    iqdata = np.vstack((IData, QData)).reshape((-1,), order='F')    # Interleave I & Q
    iqdata = iqdata * 32767                                         # scale to 7bit number
    bits  = np.array(iqdata, dtype='>i2')                           # Convert to big-endian 2byte int
    # ## ASCII + Binary
    cmd   = bytes(scpi, 'utf-8') + bits.tobytes()                   # Add ASCII + Bin

    tick = timeit.default_timer()
    K2.writeBin(cmd)
    K2.write(f'SOUR1:BB:ARB:WAV:CLOC "/var/user/{fileName}.wv",{clock}') # Set Fs/Clk Rate
    K2.write(f'BB:ARB:WAV:SEL "/var/user/{fileName}.wv"')                # Select Arb File
    testtime = timeit.default_timer() - tick

    samples = len(IData)
    rate = int(numBytes) / testtime / 1e6
    freq = 'Freq'

    data = f'{freq:9s},{clock/1e6:7.2f},{samples / clock * 1e3:7.2f},Bin SCPI,'\
        f'{samples:8d},{numBytes:10s},{numBytes:10s},'\
        f'{testtime*1000:11.3f},{rate:12.3f}'
    print(data)

def main():
    global fileName, K2

    IData, QData = readFile()
    fileName = 'iSck_VSG_IQ_Timing'

    K2 = iSocket().open('192.168.58.115', 5025)
    K2.s.settimeout(5)
    header = 'Freq[GHz],Fs[MHz],PlyTime,Transfer,IQ Pairs,Bytes Calc,Bytes Read,TTime[msec],Rate[MB/sec]'
    print(header)

    # for i in [61440, 61440, 36864, 12288, 6144, 3686, 1229, 614, 369, 123]:
    for i in [12288, 6144, 3686, 1229, 614, 369, 123]:

        tick = timeit.default_timer()
        IOut = IData * (i - 1)
        QOut = QData * (i - 1)

        testtime = timeit.default_timer() - tick
        if testtime > 5:
            print(f'Array {i} {testtime}')

        IQ_Write(IOut, QOut, 122.88e6)

if __name__ == "__main__":
    main()
