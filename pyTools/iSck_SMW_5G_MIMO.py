""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# 测试仪器
# 测量仪
# #############################################################################
# ## Main Code
# #############################################################################
仪器 = iSocket().open('192.168.58.115', 5025)
仪器.s.settimeout(2)
仪器.write(':ENT3:SOUR1:BB:NR5G:NODE:NCAR 2')               # Num CC in BB
仪器.write(':ENT3:SOUR1:BB:NR5G:NODE:CELL0:DFR -50e6')      # CC1 offset
仪器.write(':ENT3:SOUR1:BB:NR5G:NODE:CELL1:DFR +50e6')      # CC2 Offset
仪器.write(':ENT3:SOUR1:BB:NR5G:NODE:CARM:CARR1:ROW0 1')    # CC Mapping
仪器.write(':ENT3:SOUR1:BB:NR5G:NODE:CARM:CARR1:ROW1 1')    # CC Mapping
仪器.write(':ENT3:SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:PDSCh:TXSC:NLAY 1')      # 
仪器.write(':ENT3:SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:PDSCh:TXSC:NLAY 2')      # 
仪器.write(':ENT3:SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:APM:COL0:ROW1:REAL 1')      # 
