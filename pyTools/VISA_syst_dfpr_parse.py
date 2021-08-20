"""Parse R&S SYST:DFPR String"""
from iVISA import iVISA
from xml.etree import ElementTree as ET

# #############################################################################
# ## Code Begin
# #############################################################################
K2      = iVISA().open('192.168.58.109')
rdStr   = K2.query('SYST:DFPR?')
XMLstr  = '<' + rdStr.split('<', 1)[1]
# print(XMLstr)

if rdStr == '<notRead>':
    print('Instrument not supported')
else:
    root_element = ET.fromstring(XMLstr)

    for child in root_element:
        print(child)
        for key, value in child.attrib.items():
            print(f'    {key}:{value}')
