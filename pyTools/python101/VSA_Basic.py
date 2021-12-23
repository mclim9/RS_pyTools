""" Spectrum Analyzer Demo"""
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    sOut = s.recv(100000).decode().strip()  # Read socket
    return sOut

def sWrite(SCPI):                           # Socket Write
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

def getData(freq):
    sWrite(f':SENS:FREQ:CENT {cFreq}')      # Center Frequency
    sQuery('INIT:IMM;*OPC?')  # 10 sec sweep
    sWrite(':CALC1:MARK1:MAX:PEAK')
    mkrPower = sQuery(':CALC1:MARK1:Y?')
    return f'{freq},{mkrPower}'


# ## Main Code
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(5)                             # Timeout in seconds
print(sQuery(f'*IDN?'))

cFreq = 2400e6
freqList = [-450e3, -350e3, -250e3, -150e3, -100e3, 100e3, 200e3, 300e3, 400e3, 450e3]

sWrite('FORM:DATA ASCII')
sWrite(f':SENS:FREQ:CENT {cFreq}')          # Center Frequency
sWrite(':SENS:FREQ:SPAN 0')                 # Span
sWrite(':SENS:BAND:RES 100kHz')             # Res Bandwidth
sWrite(':SENS:BAND:VID 300kHz')             # Video Bandwidth
sWrite(':SENS:SWE:TIME 100ms')              # Sweep time

sWrite('INIT:CONT OFF')                     # Continuous Sweep Off
sWrite(':DISP:TRAC:Y:RLEV 0')               # Ref Level
sWrite(':INP:ATT:AUTO ON')                  # Attenuation: Auto
sWrite(':INP:ATT 10')                       # Attenuation: 10dB
sWrite(':SENS:WIND1:DET1:FUNC AVER')        # Detector
sWrite(':DISP:WIND1:TRAC1:MODE MAXH')       # MaxHold
sWrite(':SENS:AVER:COUN 10')                # Average Count
sWrite(':SENS:AVER:TYPE POW')               # Average Method

data = []
data.append(getData(cFreq))

for freqOffset in freqList:
    data.append(getData(cFreq + freqOffset))

print(data)
