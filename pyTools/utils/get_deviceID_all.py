""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module
import logging
import platform

logging.basicConfig(level=logging.INFO,
                    filename=__file__.split('.')[0] + '.log', filemode='a',
                    format='%(asctime)s - %(message)s')
logging.info(platform.node())

def sQuery(SCPI):                           # Socket Query
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
    sOut = s.recv(100000).decode().strip()  # Read socket
    print(sOut)
    return sOut

def getSysInfo():
    s.sendall(f'SYST:DFPR?;*OPC?\n'.encode())
    xmlIn = s.recv(1000000).decode().strip()  # Read socket
    strStart = xmlIn.find('deviceId="') + len('deviceID="')
    # strStop  = xmlIn.find('type="') - 2
    strStop  = strStart + 22
    xmlIn = xmlIn[strStart:strStop]          # Remove header
    print(xmlIn)
    return xmlIn

def getHwList():
    s.sendall(f'SYST:DFPR?\n'.encode())
    xmlIn = s.recv(1000000).decode().strip()  # Read socket
    # strSearch = '<HardwareData>'
    # strStart = xmlIn.find(strSearch) + len(strSearch)
    # strStop  = xmlIn.find('</HardwareData>')
    # xmlIn = xmlIn[strStart:strStop]          # Remove header
    # print(xmlIn)
    return xmlIn

ipArry = ['192.168.1.108',
          '192.168.1.109',
          '192.168.1.114',
          '192.168.1.115',
          '192.168.1.116',
          '192.168.58.109',
          '192.168.58.114',
          '192.168.58.115']

for inst in ipArry:
    s = socket.socket()                         # Create a socket object
    try:
        s.connect((inst, 5025))
        s.settimeout(10)                             # Timeout in seconds
        logging.info(f"{sQuery('*IDN?')}")
        # logging.info(f"{sQuery('*OPT?')}")
        logging.info(getSysInfo())
        logging.info(getHwList())
        s.close()
    except WindowsError:
        pass
