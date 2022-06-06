""" Rohde & Schwarz Automation for demonstration use."""
import socket

s = socket.socket()
s.connect(('192.168.58.114', 5025))
s.settimeout(5)

SCPI = '*IDN?'
s.sendall(f'{SCPI}\n'.encode())             # Write SCPI
sOut = s.recv(100000).decode().strip()      # Read socket
print(sOut)
