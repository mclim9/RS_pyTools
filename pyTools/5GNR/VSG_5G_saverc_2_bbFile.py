""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):
    sWrite(SCPI)
    return s.recv(100000).decode()          # Read socket

def sWrite(SCPI):
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.103', 5025))

for entity in [1, 2, 3, 4]:
    filename = f'DebugSetting_BB{entity}'
    sWrite(f':ENT{entity}:SOUR1:BB:NR5G:SETT:STOR "/var/user/{filename}"')
    sWrite(f':ENT{entity}:SOUR1:BB:NR5G:ANAL:CONT "/var/user/{filename}"')
