""" Rohde & Schwarz Automation for demonstration use."""

import socket

def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')                 # Print SCPI
    s.sendall(f'{SCPI}\n'.encode())         # Send SCPI

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)                            # Write SCPI
    sOut = s.recv(100000).decode().strip()  # Read SCPI
    print(f'Query: {sOut}')                 # Print sOut
    return sOut                             # Return value

s = socket.socket()
s.connect(('192.168.58.109', 5025))
s.settimeout(5)

def setup(fband='BAND1', fstart=100, fstop=5e6, caprange="NORM", measquality="NORM", fcent=2402 * 1e6):
    sWrite("*RST;*CLS;*WAI")
    sWrite("FREQ:CENT {}".format(fcent))
    sWrite("INST:CRE PNO,'Phase Noise'")
    sWrite("SENSe:FREQuency:VERify OFF")
    sWrite("SENSe:FREQuency:STARt {}".format(fstart).upper())
    sWrite("SENSe:FREQuency:STOP {}".format(fstop).upper())

setup()
