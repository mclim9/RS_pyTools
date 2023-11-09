import socket                                   # Import socket module

def sWrite(SCPI):
    try:
        s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
    except socket.error as errr:
        print(f'{SCPI} not write {errr}')

def sQuery(SCPI):
    try:
        s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
        sOut = s.recv(100000).decode().strip()  # Read socket
    except socket.error as errr:
        sOut = f'{SCPI} not Read {errr}'
    print(sOut)
    return sOut

if __name__ == '__main__':
    FSW_IP = '192.168.58.109'

    s = socket.socket()
    s.connect((FSW_IP, 5025))
    s.settimeout(5)
    sQuery(f'*IDN?')
    sWrite(f':CONF:NR5G:MEAS MCAClr')
    sWrite(f':CONF:NR5G:NOCC 8')
    sWrite(f':CONF:NR5G:OREL GMCF')
    sWrite(f':CONF:NR5G:GMCF 25000000000')
    sWrite(f':CONF:NR5G:CENT')
    # sWrite(f':CONF:NR5G:GMCF 25000000000')
    # sWrite(f':CONF:NR5G:CENT')
