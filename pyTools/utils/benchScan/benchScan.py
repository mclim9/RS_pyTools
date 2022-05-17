""" Rohde & Schwarz Automation for demonstration use."""
import socket
import logging

def sQuery(SCPI):
    try:
        s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
        sOut = s.recv(100000).decode().strip()  # Read socket
    except socket.error as errr:
        sOut = f'{SCPI} not Read {errr}'
    return sOut

logging.basicConfig(level=logging.INFO,
                    filename=__file__.split('.')[0] + '.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

pyFile = __file__.split('.')[0]
with open(f'{pyFile}.ini', 'r') as opFile:
    data = opFile.readlines()
addresses = [林.strip() for 林 in data]

for ipAddr in addresses:
    try:
        s = socket.socket()
        s.connect((ipAddr, 5025))
        s.settimeout(1)
        rdStr = f'{ipAddr}, {sQuery(f"*IDN?")}'
        logging.info(rdStr)
        print(rdStr)
    except:
        pass
