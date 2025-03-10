import socket
import tkinter as tk
from tkinter import messagebox, simpledialog

def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')                 # Print SCPI to screen
    s.sendall(f'{SCPI}\n'.encode())         # Send SCPI to socket

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)                            # Write SCPI
    sOut = s.recv(100000).decode().strip()  # Read SCPI from socket
    print(f'Query: {sOut}')                 # Print Read to screen
    return sOut                             # Return value

def main():
    root = tk.Tk()                          # Root window
    root.withdraw()                         # Invisible Root
    value = simpledialog.askstring(title='Enter IP Address',
                                   prompt='IDN IP',
                                   initialvalue='172.24.225.114')

    global s
    s = socket.socket()                     # Create Socket
    s.connect((value.strip(), 5025))        # IP Address of socket
    s.settimeout(5)                         # Timeout
    rdStr = sQuery('*IDN?')                 # Instrument Identification String

    messagebox.showinfo('IDN Return Value', f'IP :{value} IDN:{rdStr.strip()}')
    root.destroy

if __name__ == "__main__":
    main()