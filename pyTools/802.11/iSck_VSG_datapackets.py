""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

def set_data():
    number = 5
    s.write(f':SOUR1:BB:WLNN:FBL1:USER1:MPDU1:COUN {number}')
    for i in range(number):
        s.write(f':SOUR1:BB:WLNN:FBL1:USER1:MPDU{i+1}:DATA:LENG 16384')
        s.write(f':SOUR1:BB:WLNN:FBL1:USER1:MPDU{i+1}:DATA:SOUR PN23')

if __name__ == "__main__":
    s = iSocket().open('192.168.58.114', 5025)
    set_data()
