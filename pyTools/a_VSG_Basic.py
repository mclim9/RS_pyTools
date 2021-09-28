""" Basic Generator Code """
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    sOut = s.recv(100000).decode().strip()  # Read socket
    return sOut

def sWrite(SCPI):                           # Socket Write
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object
s.connect(('192.168.58.114', 5025))
s.settimeout(5)                             # Timeout in seconds

sWrite(':SOUR1:FREQ:CW 24.0e9')             # Center Freq
sWrite(':SOUR1:POW:POW 0')                  # RMS Power

arbFile = '/var/user/stock/CW__I_0_25__Q_0.wv'
sWrite(f':SOUR1:BB:ARB:WAV:SEL "{arbFile}"')    # Select Arb File
sWrite(':SOUR1:BB:ARB:STAT 1')              # BB1 Arb On
sWrite(':OUTP1:STAT 1')                     # RF1 Output On
sWrite(':SOUR1:IQ:STAT 1')                  # IQ Mod1 On
print(sQuery(f'*IDN?'))
