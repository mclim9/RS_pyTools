""" Rohde & Schwarz Automation for demonstration use."""
import os
import socket

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

s = socket.socket()
s.connect((SMW_IP, 5025))
s.settimeout(5)
sQuery(f'*IDN?')
data = sQuery(f'*OPT?').split(',')
for a in data:
    if '-B' in a:
        print(a)
os.system(f'start \\\\{SMW_IP}\\user')

# s = socket.socket()
# s.connect((FSW_IP, 5025))
# s.settimeout(5)
# sQuery(f'*IDN?')
# sQuery(f'*OPT?')
# os.system(f'start \\\\{FSW_IP}\\instr')
