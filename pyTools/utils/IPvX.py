import socket
import subprocess

def local_computer_IP():
    data = subprocess.Popen("ipconfig", stdout=subprocess.PIPE).stdout.read().decode()
    data = data.split('\r\n')
    for line in data:
        if 'adapter' in line:
            currAdapt = line
        if 'IPv6' in line:
            print(f'{currAdapt:30} {line.split(": ")[1]}')
        if 'IPv4' in line:
            print(f'{currAdapt:30} {line.split(": ")[1]}')

def idn_IPv4(IPv4):
    s = socket.socket()                         # Create a socket object
    s.connect((IPv4, 5025))
    s.sendall(f'*IDN?\n'.encode())              # Write SCPI
    sOut = s.recv(100000).decode().strip()      # Read socket
    print(sOut)
    s.close()

def idn_IPv6(IPv6):
    s = socket.socket()                         # Create a socket object
    s.connect((IPv6, 80, 0, 0))
    s.sendall(f'*IDN?\n'.encode())              # Write SCPI
    sOut = s.recv(100000).decode().strip()      # Read socket
    print(sOut)
    s.close()

def ping_iP(IPAddy):
    data = subprocess.Popen(f"ping {IPAddy}", stdout=subprocess.PIPE).stdout.read().decode()
    data = data.split('\r\n')
    print()
    for line in data:
        if 'stat' in line:
            print(line)
        if 'Sent' in line:
            print(line)
        if 'Mini' in line:
            print(line)

if __name__ == '__main__':
    local_computer_IP()
    ping_iP('192.168.58.204')
    ping_iP('fe80::72f8:939b:1e87:ff9a')
    # idn_IPv4('192.168.58.109')
    # idn_IPv6('fe80::2e0:33ff:fe0b:e1bb')
