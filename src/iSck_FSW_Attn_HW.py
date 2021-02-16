""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket

# #############################################################################
# ## Main Code
# #############################################################################
if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    print(f"AC/DC  : {s.query('DIAG:INFO:CCO? ACDC')}")
    print(f"Attn5  : {s.query('DIAG:INFO:CCO? ATT5')}")
    print(f"Attn10 : {s.query('DIAG:INFO:CCO? ATT10')}")
    print(f"Attn20 : {s.query('DIAG:INFO:CCO? ATT20')}")
    print(f"Attn40 : {s.query('DIAG:INFO:CCO? ATT40')}")
    print(f"Cal Src: {s.query('DIAG:INFO:CCO? CAL')}")
    print(f"Preamp : {s.query('DIAG:INFO:CCO? PRE')}")

    HWInfo = s.query('DIAG:SERV:HWIN?').split('","')
    for module in HWInfo:
        if 'DETECTOR EXTENSION BOARD 2' in module:
            print(module)
