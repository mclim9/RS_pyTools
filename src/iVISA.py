'''Rohde & Schwarz Automation for demonstration use.'''
import xml.etree.ElementTree as ET
import visa                             # Import VISA module

# #############################################################################
# ## Code Begin
# #############################################################################
class iVISA():
    """ instrument VISA class """
    def __init__(self):
        # self.s = socket.socket()                # Create a socket
        pass

    def close(self):
        self.VISA.close()

    def open(self, host):
        '''Open VISA session'''
        rm = visa.ResourceManager()
        # rmlist = rm.list_resources()
        self.VISA = rm.open_resource(f'TCPIP0::{host}::inst0::INSTR')

    def query(self, SCPI):
        '''VISA query'''
        vOut = self.VISA.query(SCPI)            # Query cmd
        return vOut.strip()

    def write(self, SCPI):
        '''VISA write'''
        self.VISA.write(SCPI)                   # Write cmd

    def getSysInfo(self):
        '''Get System Info'''
        xmlIn = self.query("SYST:DFPR?")

        xmlIn = xmlIn[xmlIn.find('>') + 1:]   # Remove header
        root  = ET.fromstring(xmlIn)
        if 0:
            DData = root.find('DeviceData').items()
            devID = DData[0][1]
            dType = DData[1][1]
        devID = root[0].attrib['deviceId']
        dType = root[0].attrib['type']
        print(dType, devID)

# #########################################################
# ## Main Code
# #########################################################
if __name__ == "__main__":
    v = iVISA()
    v.open('192.168.58.109')
    print(f'Info: {v.query("*IDN?")}')
    v.getSysInfo()
    v.close()
