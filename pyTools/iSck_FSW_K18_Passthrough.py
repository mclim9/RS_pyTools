import timeit
from iSocket import iSocket                                         # Import socket module

def SMW_K18_connect(ipAddr):
    s.write(f':CONF:GEN:IPC:ADDR "{ipAddr}"')
    s.write(f':CONF:GEN:CONT:STAT ON;*WAI')
    SMWconn = s.query(f':CONF:GEN:CONT:STAT?')                      # Query state
    if SMWconn == "OFF":
        s.write(f':CONF:GEN:CONT:STAT ON;*WAI')
        SMWconn = s.query(f':CONF:GEN:CONT:STAT?')                  # Query state
    return SMWconn

def SMW_K18_powerState(state):
    # ON OFF
    if state in {1, 'on', 'ON'}:
        s.write(f':CONF:GEN:RFO:STAT ON;*WAI')
    elif state in {0, 'off', 'OFF'}:
        s.write(f':CONF:GEN:RFO:STAT OFF;*WAI')
    else:
        print('SMW_K18_PowerState input not supported')

def SMW_K18_powerValue(dBm):
    s.write(f':CONF:GEN:POW:LEV {dBm};*WAI')

def SMW_K18_query(SCPI):
    s.write(f':CONF:GEN:REL:WRIT "{SCPI}"')
    rdStr = s.query(f':CONF:GEN:REL:READ?')
    # rdStr = s.query(f':CONF:GEN:REL:WRIT "{SCPI}"; READ?')
    return rdStr

def SMW_K18_write(SCPI):
    s.write(f':CONF:GEN:REL:WRIT "{SCPI}"')

if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    s.query(f':INST:SEL "Amplifier";*OPC?')
    SMW_K18_connect('192.168.58.114')
    SMW_K18_powerState('ON')
    SMW_K18_powerValue('-20')
    SMW_K18_write(':SOUR1:FREQ:CW 2e9')
    tick = timeit.default_timer()
    print(SMW_K18_query('*IDN?'))
    print(f'CmdTime: {timeit.default_timer() - tick} secs')
