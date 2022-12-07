""" Rohde & Schwarz Automation for demonstration use."""
import socket

class instr(object):
    def __init__(self, ipAddr):
        self.s = socket.socket()
        self.s.connect((ipAddr, 5025))
        self.s.settimeout(5)

    def query(self, SCPI):                           # Socket Query
        self.write(SCPI)
        sOut = self.s.recv(100000).decode().strip()
        print(f'Query: {sOut}')
        return sOut

    def write(self, SCPI):                           # Socket Write
        print(f'Write: {SCPI}')
        self.s.sendall(f'{SCPI}\n'.encode())

FSW = instr('192.168.58.115')
FSW.query('*IDN?')
FSW.query('*OPT?')
