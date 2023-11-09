""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
from vdi_power_meter import PowerMeter

SMW = iSocket().open('192.168.10.30', 5025)
VDI = PowerMeter('COM8')

def file_write(outString):
    filename = __file__.split('.')[0] + '.csv'
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    print(outString)
    fily.close()

for pwr in [-30, -20, -10, 0, 10, 20]:
    SMW.query(f':SOUR1:POW:LEV {pwr};*OPC?')
    for freq in range(int(125e9), int(153e9), int(1e9)):
        SMW.write(f':SOUR1:FREQ:CW {freq}')
        # pwrMeter = SMW.queryFloat(f'READ2:POW?')
        SMW.delay(3)
        pwrMeter = VDI.measure()
        file_write(f'{freq},Hz, {pwr},dbm, {pwrMeter}')
