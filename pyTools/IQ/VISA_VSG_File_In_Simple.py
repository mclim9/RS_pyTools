import pyvisa

# Read Source Waveform
wvName  = 'test.wv'
f       = open(wvName, 'rb')
byteAry = f.read()
f.close()

# Open VISA connection
rm      = pyvisa.ResourceManager()
instr   = rm.open_resource('TCPIP::192.168.58.114::INSTR')

# Create SCPI command scpi
numByte = len(byteAry)                          # Bytes in file
numHead = len(str(numByte))                     # Length of numByte
scpi    = f':MMEM:DATA "/var/user/wave.wv",#{numHead}{numByte}'
command = bytes(scpi, 'utf-8') + byteAry        # Create byte array

# Send commands
instr.write_raw(command)                        # Write byte data
print(instr.query('SYST:ERR?'))                 # Check for Errors
