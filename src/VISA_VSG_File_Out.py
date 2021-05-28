import pyvisa

fileName = 'CW__I_m0_25__Q_0.wv'

# Open VISA connection
rm      = pyvisa.ResourceManager()
instr   = rm.open_resource('TCPIP::192.168.58.114::INSTR')

instr.write(f'MMEMory:DATA? "/var/user/{fileName}"')
byteAry = instr.read_raw()                              # Read byte array

numByte = int(chr(byteAry[1]))                          # Number of Bytes
numIQ   = int(byteAry[2:2 + numByte])
data    = byteAry[(numByte + 2):-1]                     # Remove Header

f = open(fileName, 'wb')
f.write(data)
f.close()
