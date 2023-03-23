""" Rohde & Schwarz RTP Amplitude Measurement"""
from iSocket import iSocket                             # Import socket module

class PVT(iSocket):
    def __init__(self):
        super().__init__()

    def IDN(self):
        rdStr = self.query(f'*IDN?')
        return rdStr

    def file_write(outString):
        filename = __file__.split('.')[0] + '.csv'
        fily = open(filename, '+a')
        fily.write(f'{outString}\n')
        fily.close()

if __name__ == "__main__":
    pvt = PVT().open('192.168.58.30', 5025)
    pvt.s.settimeout(5)
    pvt.IDN()
