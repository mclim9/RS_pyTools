""" Rohde & Schwarz instr Automation for demonstration use."""
import pyvisa as visa                           # Import VISA module

rm = visa.ResourceManager()
instr = rm.open_resource(f'TCPIP0::192.168.58.109::inst0::INSTR')

chunk = 10000
instr.write('FORM:DATA REAL,32')                 # 4 bytes per I or Q
instr.write('TRAC:IQ:DATA:FORM IQP')             # IQ Pairs
recLent = int(instr.query(f':TRAC:IQ:RLEN?'))
IQData = []
for i in range(recLent // chunk):
    rdChunk  = instr.query_binary_values(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}')
    IQData += rdChunk
    endPtr = (i + 1) * chunk
if recLent - endPtr != 0:
    IQData += instr.query_binary_values(f'TRAC:IQ:DATA:MEM? {endPtr},{recLent - endPtr}')

IQPoints = len(IQData) / 2                      # 4 bytes I + 4 bytes Q
print(f'{int(IQPoints)} IQ Points')
