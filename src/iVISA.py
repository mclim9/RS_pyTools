'''Rohde & Schwarz Automation for demonstration use.'''
import xml.etree.ElementTree as ET
import logging
import pyvisa as visa                                   # Import VISA module


# #############################################################################
# ## Code Begin
# #############################################################################
class iVISA():
    """ instrument VISA class """
    def __init__(self):
        # self.s = socket.socket()                      # Create a socket
        pass

    def close(self):
        self.VISA.close()

    def open(self, host):
        '''Open VISA session'''
        try:
            logging.basicConfig(level=logging.INFO,
                        filename=__file__.split('.')[0] + '.log', filemode='a',         # noqa:
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa:
            rm = visa.ResourceManager()
            # rmlist = rm.list_resources()
            self.VISA = rm.open_resource(f'TCPIP0::{host}::inst0::INSTR')
        except visa.errors:
            print(f"VError: {visa.errors}")
        return self

    def query(self, SCPI):
        '''VISA query'''
        logging.info(f'Write> {SCPI}')
        try:
            vOut = self.VISA.query(SCPI)                    # Query cmd
            logging.info(f'Read < {vOut.strip()}')
        except:
            vOut = ''
        return vOut.strip()

    def queryFloat(self, SCPI):
        rdStr = self.query(SCPI)
        return float(rdStr)

    def queryInt(self, SCPI):
        rdStr = self.query(SCPI)
        return int(rdStr)

    def read(self):
        rdStr = self.VISA.read_raw()
        return rdStr

    def timeout(self, sec):
        self.VISA.timeout = int(sec * 1000)

    def write(self, SCPI):
        '''VISA write'''
        logging.info(f'Write> {SCPI}')
        self.VISA.write(SCPI)                           # Write cmd

    def getSysInfo(self):
        '''Get System Info'''
        xmlIn = self.query("SYST:DFPR?")

        xmlIn = xmlIn[xmlIn.find('>') + 1:]             # Remove header
        root = ET.fromstring(xmlIn)
        if 0:
            DData = root.find('DeviceData').items()
            devID = DData[0][1]
            dType = DData[1][1]
        devID = root[0].attrib['deviceId']
        dType = root[0].attrib['type']
        print(dType, devID)


# #############################################################################
# ## Main Code
# #############################################################################
if __name__ == "__main__":
    v = iVISA()
    v.open('192.168.58.109')
    print(f'Info: {v.query("*IDN?")}')
    v.getSysInfo()
    v.close()
