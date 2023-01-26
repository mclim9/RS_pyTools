"""Rohde & Schwarz instrument socket for demonstration use."""
import logging
import socket
import os


class iSocket():
    """ instrument socket class """
    def __init__(self):
        self.s = socket.socket()                    # Create a socket

    def close(self):
        self.s.close()

    def delay(self, seconds):
        pass
        # time.sleep(seconds)

    def open(self, host, port):                     # noqa: E302
        """connect instrument socket"""
        try:
            logging.basicConfig(level=logging.INFO,
                                filename=__file__.split('.')[0] + '.log', filemode='a',         # noqa:
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa:
        except socket.error:
            pass
        return self

    def opc(self, SCPI):
        pass

    def write(self, SCPI):                          # noqa: E302
        """Socket Write"""
        logging.info(f'Write> {SCPI.strip()}')

    def writeBin(self, SCPI):                       # noqa: E302
        """Socket Write"""
        logging.info(f'Write> {SCPI.strip()}')

    def query(self, SCPI):                          # noqa: E302
        """Socket Query"""
        self.write(SCPI)
        sOut = 'SCPI:RET:STR'
        logging.info(f'Read < {sOut}')
        return sOut

    def queryBin(self, SCPI):
        self.write(SCPI)
        sOut = 'asdf'
        return sOut

    def queryFloat(self, SCPI):
        rdStr = self.query(SCPI)
        rdStr = '123456.789'
        return float(rdStr)

    def queryInt(self, SCPI):
        rdStr = self.query(SCPI)
        rdStr = '123456'
        return int(rdStr)

    def read(self):
        n = 10000000
        try:
            sOut = bytearray()
            while len(sOut) < n:
                packet = self.s.recv(n - len(sOut))
                if not packet:
                    return None
                sOut.extend(packet)
                if sOut[-1] == 10:
                    # sOut = sOut.decode()
                    break
        except socket.error:
            sOut = '<not Read>'
        return sOut

    def read_SCPI_file(self, filename):
        '''read SCPI array from file'''
        SCPIFile = os.path.splitext(filename)[0] + '.txt'
        SCPIOut = []
        with open(SCPIFile, 'r') as csv_file:
            fileData = csv_file.readlines()
            for line in fileData:
                if line[0] != "#":                  # Remove Comments
                    SCPIOut.append(line)
        return SCPIOut

    def send_SCPI_arry(self, SCPIarry):
        '''send SCPI array.  Check error after each cmd'''
        for cmd in SCPIarry:
            try:
                if '?' in cmd:
                    self.query(cmd)
                else:
                    self.write(cmd)
                error = self.query('SYST:ERR?')
                outStr = f'{error.strip()} {cmd.strip()}'
                logging.info(outStr)
            except socket.timeout:
                error = 'SCPI TIMEOUT' + self.query('SYST:ERR?')
                outStr = f'{error.strip()} {cmd.strip()}'
                logging.error(outStr)

    def timeout(self, seconds):
        self.s.settimeout(seconds)

# #########################################################
# ## Main Code
# #########################################################
if __name__ == "__main__":
    instr = iSocket().open('192.168.58.109', 5025)
    instr.opc('INIT:IMM')
    print(instr.query('*IDN?'))
