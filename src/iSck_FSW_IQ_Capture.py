""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
import matplotlib.pyplot as plt
import numpy as np

def Get_IQ_Data_Ascii(MLEN=1000):
    CSVd = []
    FSW.write('Format:DATA ASCII')
    FSW.write('TRAC:IQ:DATA:FORM IQP')
    RLEN = FSW.queryInt('TRAC:IQ:RLEN?')                    # Sweep Points
    numLoops  = int(round(RLEN / MLEN))
    for i in range(numLoops):
        SCPI = f"TRAC:IQ:DATA:MEM? {i * MLEN},{MLEN}"       # TRAC:IQ:DATA:MEM? <MemStrt>,<MLEN>
        FSW.write(SCPI)
        Data = FSW.read().split(',')
        if len(Data) != 2 * MLEN:
            FSW.write(SCPI)
            Data = FSW.read().split(',')
            print('ReRead')
        CSVd.extend(Data)
    print(f"Memory Done Reading {len(CSVd)}")
    return CSVd

def Get_IQ_Data_Bin():
    import struct
    FSW.write('FORMAT:DATA REAL,32')
    FSW.write('TRAC:IQ:DATA:FORM IQP')
    FSW.write('TRAC:IQ:DATA:MEM?')
    rdStr = FSW.read()
    numBytes = int(chr(rdStr[1]))                           # Number of Bytes
    numIQ    = int(rdStr[2:2 + numBytes])
    IQBytes  = rdStr[(numBytes + 2):-1]                     # Remove Header
    IQAscii  = struct.unpack("<" + 'f' * int(numIQ / 4), IQBytes)
    print(IQAscii[0:10])
    return IQBytes

def plot_IQ_FFT(IData, QData):
    # ######################################
    # ### Calculate FFT
    # ######################################
    IQ = np.asarray(IData) + 1j * np.asarray(QData)
    IQlen = len(IData)

    mag = np.fft.fft(IQ) / IQlen
    mag = np.fft.fftshift(mag)                                          # ag = mag[range(N/2)]

    frq = np.fft.fftfreq(IQlen, d=1 / (1.6e9))
    frq = np.fft.fftshift(frq)                                          # frq = frq[range(N/2)]

    # ######################################
    # ### Plot Data
    # ######################################
    plt.clf()
    plt.subplot(2, 1, 1)                                                # Time Domain
    plt.title("Time Domain I:Blue Q:Yellow")
    plt.plot(IData, "b", IData, "b")
    plt.plot(QData, "y", QData, "y")

    plt.subplot(2, 1, 2)                                                # Frequency Domain
    # if self.IQpoints:
    #     plt.plot(frq, mag,'bo')
    plt.plot(frq, np.real(mag))
    plt.xlabel('Freq')
    plt.ylabel('magnitude')
    plt.grid(True)
    plt.show()

def deInterlace(iqData):
    IData = []
    QData = []
    length = int(len(iqData) / 2) - 1
    # length = 1000
    for i in range(length):
        IData.append(iqData[2 * i])
        QData.append(iqData[2 * i + 1])
    IData = list(map(float, IData))
    QData = list(map(float, QData))
    return (IData, QData)

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)
Freq = 4e9
Samp = 1.6e9
# waveform is 50uSec

FSW.write('*CLS')
FSW.write(':INST:SEL "IQ Analyzer"')        # Select Analog Demod
FSW.write(f':SENS:FREQ:CENT {Freq}')        # Center Frequency
FSW.write(f':TRAC:IQ:SRAT {Samp}')          # Sampling Rate
FSW.write(':SENS:SWE:TIME 0.000050')          # Capture time
FSW.query(':INIT:IMM;*OPC?')
numData = FSW.queryInt('TRAC:IQ:RLEN?')
print(f'Number IQ Data: {numData} ASCII:{numData * 18}')

CSVd = Get_IQ_Data_Ascii()
# CSVd = Get_IQ_Data_Bin()
output = deInterlace(CSVd)
plot_IQ_FFT(output[0], output[1])
