""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                     # Import socket module
from math import sqrt, log10

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)

time = 2e-6

FSW.write(':LAY:REPL:WIND "2",RIMAG')
FSW.write(f':CALC1:MARK1:X {time}')
FSW.write(f':CALC2:MARK1:X {time}')
dBm  = FSW.queryFloat(':CALC1:MARK1:Y?')
volt = FSW.query(':CALC2:MARK1:Y?')
volt = volt.split(',')
i_volt = float(volt[0])
q_volt = float(volt[1])
iq_mag = sqrt(i_volt * i_volt + q_volt * q_volt)
iq_pwr = iq_mag * iq_mag / 50
iq_dBm = 10 * log10(iq_pwr / 0.001)

print(f'dBm marker: {dBm:10.5f}')
print(f'I Voltage : {i_volt}')
print(f'Q Voltage : {q_volt}')
print(f'calc markr: {iq_dBm:10.5f}')
