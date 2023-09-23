""" Rohde & Schwarz Automation for demonstration use."""
import math
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    return s.recv(1000000).decode()         # Read socket

def sWrite(SCPI):                           # Socket Write
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(10)                            # Timeout in seconds

sWrite('FORM:DATA ASCII')                   # ASCII Format
sWrite('TRAC:IQ:DATA:FORM IQP')             # IQ Pairs
rdStr = sQuery(f'TRAC:IQ:DATA:MEM?').strip()
IQPoints = [float(value) for value in rdStr.split(',')]

numIQ = int(len(IQPoints) / 2)              # 4 bytes I + 4 bytes Q
print(f'{numIQ} IQ Points')

for i in range(numIQ):
    mag_volt = math.sqrt(IQPoints[i] * IQPoints[i] + IQPoints[i + 1] * IQPoints[i + 1])
    pwr_watt = mag_volt * mag_volt / 50
    pwr_dBm  = 10 * math.log10(pwr_watt / 0.001)
    # print(f'{mag_volt:.6f}v, {pwr_watt:.3E}W, {pwr_dBm:.2f} dBm ')
