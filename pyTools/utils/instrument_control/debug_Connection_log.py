""" Rohde & Schwarz Automation for demonstration use."""
import pyvisa as visa
import logging
import time


def startLog():
    filename = __file__.split('.')[0] + '.log'
    logging.basicConfig(level=logging.INFO,
                filename=filename, filemode='a',                                # noqa:
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa:

def write(outText):
    logging.info(f'{outText}')

def vQuery(SCPI):                           # Socket Query
    vWrite(SCPI)
    sOut = instr.query(SCPI)
    print(f'Query: {sOut}')
    return sOut

def vWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    instr.write(SCPI)
    time.sleep(0.001)

if __name__ == "__main__":
    startLog()
    rm = visa.ResourceManager()
    instr = rm.open_resource(f'TCPIP0::10.0.0.60::inst0::INSTR')
    # s.settimeout(5)

    for i in range(1000):
        time.sleep(1)                       # seconds
        rdStr = vQuery(f'*IDN?')
        rsStr = rdStr.replace('/n', '')
        logging.info(f'{rdStr}')
