""" Rohde & Schwarz Automation for demonstration use."""
import socket

class iSocket():
    """ instrument socket class """
    def __init__(self):
        self.s = socket.socket()                # Create a socket

    def close(self):
        self.s.close()

    def open(self, host, port):                 # noqa: E302
        """connect instrument socket"""
        try:
            self.s.connect((host, port))
            self.s.settimeout(1)                # Timeout(seconds)
        except socket.error:
            print(f"SckErr: {socket.error}")
        return self

    def write(self, SCPI):                      # noqa: E302
        """Socket Write"""
        print(f'Write> {SCPI.strip()}')
        self.s.sendall(f'{SCPI}\n'.encode())    # Write 'SCPI'

    def query(self, SCPI):                      # noqa: E302
        """Socket Query"""
        self.write(SCPI)
        try:
            sOut = self.s.recv(40000).strip()    # Read socket
            sOut = sOut.decode()
        except socket.error:
            sOut = '<not Read>'
        print(f'Read < {sOut}')
        return sOut

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
FSW.query('SYST:DEV:ID?')
FSW.write("SYST:COMM:NETW:IPAD '169.254.58.109'")
SMW = iSocket().open('192.168.58.114', 5025)
SMW.write(":SYST:COMM:NETW:IPAD '169.254.58.114'")
