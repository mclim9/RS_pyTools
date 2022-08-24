""" Rohde & Schwarz Automation for demonstration use """
from iSocket import iSocket                 # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)
clock       = 122.88e6
captureTime = 0.001

FSW.write('*CLS')
FSW.write(':INST:SEL "IQ Analyzer"')        # Select Analog Demod
FSW.write(':LAY:REPL:WIND "1",FREQ')
FSW.write(':SENS:WIND1:DET1:FUNC RMS')
# FSW.write(f':SENS:FREQ:CENT {Freq}')        # Center Frequency
FSW.write(f':TRAC:IQ:SRAT {clock}')         # Sampling Rate
FSW.write(f':SENS:SWE:TIME {captureTime}')  # Capture time
FSW.query(':INIT:IMM;*OPC?')

