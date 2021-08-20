'''RSSD VSA VSG Demo'''
# from rssd.VSA.Common import VSA
from rssd.VSG.Common import VSG

SMW = VSG().jav_Open('192.168.58.115')
print(SMW.query('*IDN?'))
