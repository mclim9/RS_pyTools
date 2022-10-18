""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
FSW.timeout(5)

FSW.write(':INST:SEL "Spectrum"')           # Select Analog Demod
FSW.write(':INIT:CONT OFF')                 # Single Sweep
FSW.write(':FORM:DATA ASCII')               # ASCII Output

chunk = 100
trace = ''
points = FSW.queryInt(':SENS:SWE:WIND:POIN?')
for i in range(points // chunk):
    rdChunk  = FSW.query(f'TRAC:DATA:MEM? TRACE1,{i * chunk},{chunk}')
    if len(rdChunk) < chunk * 18 - 1:
        rdChunk  = FSW.query(f'TRAC:DATA:MEM? TRACE1,{i * chunk},{chunk}')
        print(f'reread chunk{i}')
    trace += rdChunk + ','

print(f'Points: {len(trace.split(","))}')
