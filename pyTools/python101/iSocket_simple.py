"""Rohde & Schwarz instrument socket for demonstration use."""
import socket
import time


class iSocket():
    """ instrument socket class """
    def __init__(self):
        self.s = socket.socket()                    # Create a socket

    def close(self):
        self.s.close()

    def delay(self, seconds):
        time.sleep(seconds)

    def open(self, host, port):                     # noqa: E302
        """connect instrument socket"""
        try:
            self.s.connect((host, port))
            self.s.settimeout(5)                    # Timeout(seconds)
            self.idn = self.query('*IDN?')
            print(f'IDN  : {self.idn}')
        except socket.error:
            print(f"SckErr: {socket.error}")
        return self

    def opc(self):
        self.write("*ESE 1")               # Event Status Enable
        self.write("*SRE 32")              # SRE Def: Bit5:Std Event
        self.write("INIT:IMM;*OPC")        # *OPC will trigger ESR
        read = 0
        while (read & 1) != 1:             # Loop until done
            read = self.queryInt("*ESR?")     # Poll ESB
            time.sleep(0.5)
            # if time.delta > 300:           # Timeout
            #     break

    def write(self, SCPI):                          # noqa: E302
        """Socket Write"""
        self.s.sendall(f'{SCPI}\n'.encode())        # Write 'SCPI'

    def query(self, SCPI):                          # noqa: E302
        """Socket Query"""
        self.write(SCPI)
        time.sleep(.001)
        try:
            sOut = self.s.recv(10000000).strip()    # Read socket
            sOut = sOut.decode()
        except socket.error:
            sOut = '<not Read>'
        return sOut

    def queryInt(self, SCPI):
        rdStr = self.query(SCPI)
        return int(rdStr)

    def timeout(self, seconds):
        self.s.settimeout(seconds)

# #########################################################
# ## Main Code
# #########################################################
if __name__ == "__main__":
    instr = iSocket().open('192.168.58.109', 5025)
    instr.opc()
    print(instr.query('*IDN?'))
