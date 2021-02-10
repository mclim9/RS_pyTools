"""Rohde & Schwarz Automation for demonstration use. """
#pylint: disable=invalid-name

import socket                                  # Import socket module

###############################################################################
### Code Begin
###############################################################################
def sQuery(SCPI):
    """Socket Query"""
    print(f'Write: {SCPI}')
    out = SCPI + "\n"
    s.sendall(out.encode())                     # Write 'cmd'
    sOut = s.recv(2048).strip()                 # read socket
    sOut = sOut.decode()
    print(f'Query: {sOut}')
    return sOut

def sWrite(SCPI):
    """Socket Write"""
    print(f'Write: {SCPI}')
    out = SCPI + "\n"
    s.sendall(out.encode())                     # Write 'cmd'


# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                             # Create a socket object
s.connect(('192.168.58.109', 5025))
s.settimeout(1)                                 # Timeout in seconds

print("Info : " + sQuery("*IDN?"))
print("Opts : " + sQuery("*OPT?"))
