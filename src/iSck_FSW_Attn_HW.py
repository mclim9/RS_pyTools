""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket

# #############################################################################
# ## Main Code
# #############################################################################
if __name__ == "__main__":
    s = iSocket().sOpen('192.168.58.109', 5025)
    print(f"AC/DC  : {s.sQuery('DIAG:INFO:CCO? ACDC')}")
    print(f"Attn5  : {s.sQuery('DIAG:INFO:CCO? ATT5')}")
    print(f"Attn10 : {s.sQuery('DIAG:INFO:CCO? ATT10')}")
    print(f"Attn20 : {s.sQuery('DIAG:INFO:CCO? ATT20')}")
    print(f"Attn40 : {s.sQuery('DIAG:INFO:CCO? ATT40')}")
    print(f"Cal Src: {s.sQuery('DIAG:INFO:CCO? CAL')}")
    print(f"Preamp : {s.sQuery('DIAG:INFO:CCO? PRE')}")

    HWInfo = s.sQuery('DIAG:SERV:HWIN?').split('","')
    for module in HWInfo:
        if 'DETECTOR EXTENSION BOARD 2' in module:
            print(module)
