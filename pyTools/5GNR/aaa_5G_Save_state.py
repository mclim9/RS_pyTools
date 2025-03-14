""" Rohde & Schwarz Automation for demonstration use."""
import os
import socket                               # Import socket module

def sQuery(SCPI):
    try:
        s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
        sOut = s.recv(100000).decode().strip()  # Read socket
    except socket.error as errr:
        sOut = f'{SCPI} not Read {errr}'
    print(sOut)
    return sOut

def VSG_Save_5G_state():
    s.connect((SMW_IP, 5025))
    s.settimeout(5)
    sQuery(f'*IDN?')
    Band = sQuery(':SOUR1:BB:NR5G:NODE:CELL0:CARD?')
    Dir  = sQuery(':SOUR1:BB:NR5G:LINK?')
    BW   = sQuery(':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
    if Dir == 'UP':
        SCS  = sQuery(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:SCSP?')
        Mod  = sQuery(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MOD?')
        RBN  = sQuery(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN?')
        Dir  = 'UL'
    elif Dir == 'DOWN':
        SCS  = sQuery(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:DL:BWP0:SCSP?')
        Mod  = sQuery(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:MOD?')
        RBN  = sQuery(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:RBN?')
        Dir  = 'DL'

    Wavename = f'{Band}_{Dir}_{SCS}SCS_{BW}_{RBN}RB_{Mod}'
    sQuery(f':SOUR1:BB:NR5G:SETT:STOR "/var/user/{Wavename}";*OPC?')
    os.system(f'start \\\\{SMW_IP}\\user')

def VSA_Save_5G_state():
    s = socket.socket()
    s.connect((FSW_IP, 5025))
    s.settimeout(5)
    sQuery(f'*IDN?')
    sQuery(f'MMEM:STOR:DEM "C:\\R_S\\instr\\{Wavename}.allocation";*OPC?')
    os.system(f'start \\\\{FSW_IP}\\instr')

if __name__ == '__main__':
    SMW_IP = 'SMW200A-111623'
    FSW_IP = 'FSW50-101877'
    s = socket.socket()

    VSG_Save_5G_state()
    VSA_Save_5G_state()
