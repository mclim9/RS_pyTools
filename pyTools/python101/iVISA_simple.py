'''Rohde & Schwarz Automation for demonstration use.'''
import pyvisa as visa                                   # Import VISA module
import time

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
            rm = visa.ResourceManager()
            self.VISA = rm.open_resource(f'TCPIP0::{host}::inst0::INSTR')
        except visa.errors:
            print(f"VError: {visa.errors}")
        return self

    def opc(self):
        self.write("*ESE 1")               # Event Status Enable
        self.write("*SRE 32")              # SRE Def: Bit5:Std Event
        self.write("INIT:IMM;*OPC")        # *OPC will trigger ESR
        read = 0
        while (read & 1) != 1:             # Loop until done
            read = self.queryInt("*ESR?")     # Poll ESB
            time.sleep(0.5)

    def query(self, SCPI):
        '''VISA query'''
        try:
            vOut = self.VISA.query(SCPI)                    # Query cmd
        except:
            vOut = ''
        return vOut.strip()

    def queryInt(self, SCPI):
        rdStr = self.query(SCPI)
        return int(rdStr)

    def timeout(self, sec):
        self.VISA.timeout = int(sec * 1000)

    def write(self, SCPI):
        '''VISA write'''
        self.VISA.write(SCPI)                           # Write cmd


# #############################################################################
# ## Main Code
# #############################################################################
if __name__ == "__main__":
    v = iVISA()
    v.open('192.168.58.109')
    v.opc()
    v.close()
