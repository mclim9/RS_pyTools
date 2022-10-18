""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                     # Import socket module
import matplotlib.pyplot as plt
import numpy as np
# plt.switch_backend('agg')

def Get_IQ_Data_Bin():
    import struct
    FSW.write('FORMAT:DATA REAL,32')
    FSW.write('TRAC:IQ:DATA:FORM IQP')
    FSW.write('TRAC:IQ:DATA:MEM?')
    rdStr = FSW.read()
    hdrBytes = int(chr(rdStr[1]))               # Number of Bytes
    numIQ    = int(rdStr[2:2 + hdrBytes])
    IQBytes  = rdStr[(hdrBytes + 2):-1]         # Remove Header
    IQAscii  = struct.unpack("<" + 'f' * int(numIQ / 4), IQBytes)
    print(IQAscii[0:10])
    FSW.write('Format:DATA ASCII')
    return IQAscii

def plot_IQ_FFT(IData, QData, Fs):
    # ######################################
    # ### Calculate FFT
    # ######################################
    IQ = np.asarray(IData) + 1j * np.asarray(QData)
    IQlen = len(IData)

    mag = np.fft.fft(IQ) / IQlen
    mag = np.fft.fftshift(mag)                  # ag = mag[range(N/2)]
    mag = 20 * np.log10(np.abs(mag)) + 30

    print(np.where(mag == max(mag)))
    frq = np.fft.fftfreq(IQlen, d=1 / Fs)
    frq = np.fft.fftshift(frq)                  # frq = frq[range(N/2)]

    # ######################################
    # ### Plot Data
    # ######################################
    plt.clf()
    plt.subplot(2, 1, 1)                        # Time Domain
    plt.title("Time Domain I:Blue Q:Yellow")
    plt.plot(IData, "b", IData, "b")
    plt.plot(QData, "y", QData, "y")

    plt.subplot(2, 1, 2)                        # Frequency Domain
    plt.plot(frq, mag)
    plt.xlabel('Freq')
    plt.ylabel('magnitude')
    plt.grid(True)
    # plt.show(block=False)
    plt.show()
    plt.pause(2)
    plt.close()

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
Freq = 10e9
Samp = 200e6
N    = 4 * 8192
Time = N / Samp
RBW  = Samp / N
# waveform is 50uSec

FSW.write('*CLS')
FSW.write(':INST:CRE:NEW IQ, "IQ Analyzer"')    # Select IQ Analyzer
FSW.write(f':SENS:FREQ:CENT {Freq}')            # Center Frequency
FSW.write(f':TRAC:IQ:SRAT {Samp}')              # Sampling Rate
FSW.write(f':SENS:SWE:TIME {Time}')             # Capture time
FSW.query(':INIT:IMM;*OPC?')
numData = FSW.queryInt('TRAC:IQ:RLEN?')
print(f'Number IQ Data: {numData} ASCII:{numData * 18}')

CSVd = Get_IQ_Data_Bin()
output = deInterlace(CSVd)
plot_IQ_FFT(output[0], output[1], Samp)
