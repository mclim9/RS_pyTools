""" Rohde & Schwarz Automation for demonstration use."""
import os
import socket                               # Import socket module

def sQuery(SCPI):
    try:
        s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
        sOut = s.recv(100000).decode().strip()  # Read socket
    except socket.error as errr:
        sOut = f'{SCPI} not Read {errr}'
    print(sOut)
    return sOut

SMW_IP = '192.168.58.114'
FSW_IP = '192.168.58.109'
SMW_IP = '172.24.225.107'
FSW_IP = '172.24.225.128'

s = socket.socket()
s.connect((SMW_IP, 5025))
s.settimeout(5)
sQuery(f'*IDN?')
Freq = sQuery(':SOUR1:FREQ:CW?')
Freq = int(Freq)/1e9
Wavename = f'Demo-{Freq:.3f}GHz'
sQuery(f':SYST:SAV "/var/user/{Wavename}";*OPC?')
os.system(f'start \\\\{SMW_IP}\\user')

s = socket.socket()
s.connect((FSW_IP, 5025))
s.settimeout(5)
sQuery(f'*IDN?')
sQuery(f'MMEM:STOR:STAT 1,"{Wavename}";*OPC?')
os.system(f'start \\\\{FSW_IP}\\instr\\user')
