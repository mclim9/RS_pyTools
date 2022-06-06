"""Rohde & Schwarz instrument socket class example"""
import logging
import socket
import time
import os


class iSocket():
    """ instrument socket class """
    def __init__(self):
        self.s = socket.socket()                    # Create a socket
        self.close = 0

    def close(self):
        self.s.close()

    def delay(self, seconds):
        time.sleep(seconds)

    def open(self, host, port):
        """connect instrument socket"""
        try:
            if self.close == 1:
                return None
            else:
                logging.basicConfig(level=logging.INFO,
                                    filename=__file__.split('.')[0] + '.log', filemode='a',         # noqa:
                                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa:
                self.s.connect((host, port))
                self.s.settimeout(1)                    # Timeout(seconds)
                self.idn = self.query('*IDN?')
                print(self.idn)
        except socket.error:
            print(f"SckErr: {socket.error}")
        return self

    def write(self, SCPI):
        """Socket Write"""
        logging.info(f'Write> {SCPI.strip()}')
        self.s.sendall(f'{SCPI}\n'.encode())        # Write 'SCPI'

    def query(self, SCPI):
        """Socket Query"""
        if self.close == 1:
            return None
        else:
            self.write(SCPI)
            print(f'{SCPI}  ', end='')
            time.sleep(.001)
            try:
                sOut = self.s.recv(10000000).strip()    # Read socket
                sOut = sOut.decode()
            except socket.error:
                sOut = '<not Read>'
            logging.info(f'Read < {sOut}')
            print(sOut)
        return sOut

    def queryFloat(self, SCPI):
        rdStr = self.query(SCPI)
        return float(rdStr)

    def queryInt(self, SCPI):
        rdStr = self.query(SCPI)
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
    print(instr.query('*IDN?'))
