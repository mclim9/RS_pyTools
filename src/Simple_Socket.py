"""Rohde & Schwarz Automation for demonstration use. """
# pylint: disable=invalid-name
import socket                                  # Import socket module

# ##############################################################################
# ## Code Begin
# ##############################################################################
def sConnect(host, port):               # noqa: E302
    try:
        s.connect((host, port))
        s.settimeout(1)                 # Timeout(seconds)
        sQuery('*IDN?')
    except socket.error:
        print(f"SckErr: {socket.error}")

def sWrite(SCPI):                               # noqa: E302
    """Socket Write"""
    print(f'Write> {SCPI}')
    out = SCPI + "\n"
    s.sendall(out.encode())                     # Write 'SCPI'

def sQuery(SCPI):                               # noqa: E302
    """Socket Query"""
    sWrite(SCPI)
    try:
        sOut = s.recv(2048).strip()             # Read socket
        sOut = sOut.decode()
    except socket.error:
        sOut = '<not Read>'
    print(f'Read < {sOut}')
    return sOut


# ##############################################################################
# ## Main Code
# ##############################################################################
if __name__ == "__main__":
    s = socket.socket()                             # Create a socket object
    sConnect('192.168.58.109', 5025)

    print("Info : " + sQuery("*IDN?"))
    print("Opts : " + sQuery("*OPT?"))
