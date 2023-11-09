""" Rohde & Schwarz Automation for demonstration use."""
from ..iSocket import iSocket

SMW = iSocket().open('192.168.58.115', 5025)

rdStr = SMW.query(f'DIAG:BGIN?').split(',')
for optty in rdStr:
    print(optty)
