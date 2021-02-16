"""Rohde & Schwarz instrument socket for demonstration use."""
import socket
import logging

class iSocket():
    """ instrument socket class """
    def __init__(self):
        self.s = socket.socket()                # Create a socket

    def sConnect(self, host, port):             # noqa: E302
        """connect instrument socket"""
        try:
            logging.basicConfig(level=logging.INFO, \
                                filename=__file__.split('.')[0] + '.log', filemode='a', \
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.s.connect((host, port))
            self.s.settimeout(1)                # Timeout(seconds)
            print(self.sQuery('*IDN?'))
        except socket.error:
            print(f"SckErr: {socket.error}")
        return self

    def sWrite(self, SCPI):                     # noqa: E302
        """Socket Write"""
        logging.info(f'Write> {SCPI}')
        self.s.sendall(f'{SCPI}\n'.encode())    # Write 'SCPI'

    def sQuery(self, SCPI):                     # noqa: E302
        """Socket Query"""
        self.sWrite(SCPI)
        try:
            sOut = self.s.recv(2048).strip()    # Read socket
            sOut = sOut.decode()
        except socket.error:
            sOut = '<not Read>'
        logging.info(f'Read < {sOut}')
        return sOut


# #########################################################
# ## Main Code
# #########################################################
if __name__ == "__main__":
    instr = iSocket().sConnect('192.168.58.109', 5025)
    instr.sWrite(':INIT:IMM')

    print(instr.sQuery(':FETC:PNO:IPN?'))
