""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module


FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(30)

FSW.write(':SENS:FREQ:CENT 24e9')                               # Center
