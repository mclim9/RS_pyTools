"""Rohde & Schwarz Automation for demonstration use. """
from iSocket import iSocket

# ##############################################################################
# ## Main Code
# ##############################################################################
instr = iSocket().open('192.168.58.109', 5025)
# instr.s.timeout(5)                                     # Timeout in seconds
arry = instr.read_SCPI_file(__file__)
instr.send_SCPI_arry(arry)
