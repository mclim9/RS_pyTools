# https://www.rohde-schwarz.com/us/faq/how-to-automatically-transfer-iq-data-from-fsvr-spectrum-analyzer-to-vse-software-python-example-faq_78704-1023936.html
import pyvisa as visa                           # Import VISA module

rm = visa.ResourceManager()
instr = rm.open_resource(f'TCPIP0::192.168.58.109::inst0::INSTR')
instr.read_termination='\n'
instr.write_termination='\n'
instr.timeout = 5000

response = instr.query('*IDN?')
print(response)

# instr.write('FREQ:CENT 1e9')
# instr.write('DISP:TRAC:Y:RLEV 0')
# instr.write('TRAC1:IQ ON')
# instr.write('TRAC1:IQ:SRAT 32 MHZ')
# instr.write('TRAC1:IQ:RLEN 691') # Range: 1 ... 209715200(200*1024*1024)
# instr.query('*OPC?')

filePathPc = r"c:\temp\data.iq.tar"
filePathInstr = r"c:\temp\dev_data.iq.tar"

instr.write('INIT')
instr.query('*OPC?')

# save IQ-data file on instrument hard drive
instr.write(f'MMEM:STOR:IQ:STAT 1, "{filePathInstr}"')

# ask for file data from instrument and save to local hard drive
fileData = bytes(instr.query_binary_values(f'MMEM:DATA? "{filePathInstr}"', datatype='s'))
newFile = open(filePathPc, "wb")
newFile.write(fileData)
newFile.close()

print(instr.query('SYST:ERR?'))

instr.close()
