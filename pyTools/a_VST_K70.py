""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    sOut = s.recv(2048).strip().decode()    # Read socket
    print(f'Query: {sOut}')
    return sOut

def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

# ##############################################################################
# ## Main Code
# ##############################################################################
s = socket.socket()                         # Create a socket object

# # VSG Setup
s.connect(('192.168.58.114', 5025))
s.settimeout(1)                             # Timeout in seconds
sWrite(f':SOUR1:BB:DM:SRAT 1234000')        # Data rate
sWrite(f':SOUR1:BB:DM:PRBS:LENG 23')        # Data
sWrite(f':SOUR1:BB:DM:FORM QAM16')          # Modulation
sWrite(f':SOUR1:BB:DM:FILT:TYPE RCOS')      # Filter
sWrite(f':SOUR1:BB:DM:FILT:PAR:RCOS 0.123') # Filter Coeffient
sQuery(f':SOUR1:BB:DM:STAT 1;*OPC?')        # Baseband
sWrite(f'"SOUR1:IQ:STAT 1;*OPC?')           # IQ Mod
sWrite(f':OUTP1:STAT 1;*OPC?')              # RF Output
s.close()

# ## VSA Setup
s.connect(('192.168.58.109', 5025))
s.settimeout(1)                             # Timeout in seconds
sWrite(f':INST:CRE:NEW DDEM, "VSA"')        # Create Vector demod Ch
sWrite(f':SENS:DDEM:SRAT 1234000')          # Data Rate
sWrite(f':SENS:DDEM:FORM QAM')              # Set Modulation
sWrite(f':SENS:DDEM:QAM:FORM NORMal')       # Set Modulation
sWrite(f':SENS:DDEM:QAM:NST 16')            # Set Modulation
sWrite(f':SENS:DDEM:TFIL:NAME "RRC"')       # Set Filter
sWrite(f':SENS:DDEM:TFIL:ALPH 0.123')       # SEt Filter Coefficient
