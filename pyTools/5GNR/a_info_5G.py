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
ProbNm = 'FR1-UL-CP-20Mhz-30kSCS-QAM64'

s = socket.socket()
s.connect((SMW_IP, 5025))
s.settimeout(5)
sQuery(f'*IDN?')
sQuery(f':SOUR1:BB:NR5G:SETT:STOR "/var/user/{ProbNm}";*OPC?')
os.system(f'start \\\\{SMW_IP}\\user')

s = socket.socket()
s.connect((FSW_IP, 5025))
s.settimeout(5)
sQuery(f'*IDN?')
sQuery(f'MMEM:STOR:DEM "C:\\R_S\\instr\\{ProbNm}.allocation";*OPC?')
os.system(f'start \\\\{FSW_IP}\\instr')
