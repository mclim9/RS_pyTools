"""Rohde & Schwarz instrument socket for demonstration use."""
import socket
import logging
import os


class iSocket():
    """ instrument socket class """
    def __init__(self):
        self.s = socket.socket()                # Create a socket

    def sOpen(self, host, port):             # noqa: E302
        """connect instrument socket"""
        try:
            logging.basicConfig(level=logging.INFO,
                                filename=__file__.split('.')[0] + '.log', filemode='a',         # noqa:
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa:
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

    def read_SCPI_file(self, filename):
        '''read SCPI array from file'''
        SCPIFile = os.path.splitext(filename)[0] + '.txt'
        SCPIOut = []
        with open(SCPIFile, 'r') as csv_file:
            fileData = csv_file.readlines()
            for line in fileData:
                if line[0] != "#":                          # Remove Comments
                    SCPIOut.append(line)
        return SCPIOut

    def send_SCPI_arry(self, SCPIarry):
        '''send SCPI array.  Check error after each cmd'''
        for cmd in SCPIarry:
            try:
                if '?' in cmd:
                    self.sQuery(cmd)
                else:
                    self.sWrite(cmd)
                error = self.sQuery('SYST:ERR?')
                outStr = f'{error.strip()} {cmd.strip()}'
                logging.info(outStr)
            except socket.timeout:
                error = 'SCPI TIMEOUT' + self.sQuery('SYST:ERR?')
                outStr = f'{error.strip()} {cmd.strip()}'
                logging.error(outStr)


# #########################################################
# ## Main Code
# #########################################################
if __name__ == "__main__":
    instr = iSocket().sOpen('192.168.58.109', 5025)
    instr.sWrite(':INIT:IMM')

    print(instr.sQuery(':FETC:PNO:IPN?'))