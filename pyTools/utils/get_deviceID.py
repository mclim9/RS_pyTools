""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module
import logging

logging.basicConfig(level=logging.INFO,
                    filename=__file__.split('.')[0] + '.log', filemode='a',         # noqa:
                    format='%(asctime)s - %(message)s')  # noqa:

def sQuery(SCPI):                           # Socket Query
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
    sOut = s.recv(100000).decode().strip()  # Read socket
    print(sOut)
    return sOut

s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.114', 5025))
s.settimeout(1)                             # Timeout in seconds
logging.info(f"{sQuery('*IDN?')}")


s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(1)                             # Timeout in seconds
logging.info(f"{sQuery('*IDN?')}")
