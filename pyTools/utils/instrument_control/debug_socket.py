""" Rohde & Schwarz Automation for demonstration use."""
import socket

def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')                 # Print SCPI to screen
    s.sendall(f'{SCPI}\n'.encode())         # Send SCPI to socket

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)                            # Write SCPI
    sOut = s.recv(100000).decode().strip()  # Read SCPI from socket
    print(f'Query: {sOut}')                 # Print Read to screen
    return sOut                             # Return value

s = socket.socket()                         # Create Socket
s.connect(('10.0.0.35', 5025))              # IP Address of socket
s.settimeout(5)                             # Timeout

sQuery('*IDN?')                             # Instrument Identification String
# sQuery('*OPT?')                           # Query options
sWrite(':OUTP:AMOD MAN')                    # Manual Attenuation
sWrite(':SOUR1:POW:ATT -6')                 # Attn Value
sQuery('OUTP1:AFIX:RANG:LOW?')              # Poweer Range Lower
sQuery('OUTP1:AFIX:RANG:UPP?')              # Poweer Range Upper
sWrite(':SOUR1:POW:LEV:IMM:AMPL -40')       # Power Level
# sWrite(':SOUR1:POW:LEV:IMM:AMPL MIN')     # Power Level
sQuery(':SYST:ERR?')
sQuery(':SYST:ERR?')
