""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket

# #############################################################################
# ## Main Code
# #############################################################################
if __name__ == "__main__":
    s = iSocket().open('192.168.58.114', 5025)
    print(f"FacCalDate: {s.query('CAL:DATA:FACT:DATE?')}")          # Last Factory Cal
    print(f"UsrCalDate: {s.query('CAL:ALL:DATE?')}")                # UserCal Date
    print(f"UsrCalStat: {s.query('CAL:ALL:INF?')}")                 # UserCal Status
    print(f"UsrCalTemp: {s.query('CAL:ALL:TEMP?')}")                # UserCal Temp Delta
    print(f"UsrCalTime: {s.query('CAL:ALL:TIME?')}")                # UserCal Time
    print(f"PowerCycle: {s.query(':DIAG:INFO:POC?')}")              # Power count
    print(f"Options   : {s.query('*OPT?').replace(',SMW-',',')}")   # Options

    # #############################################################################
    # ## Extensive HW Info
    # #############################################################################
    # hw_cat = s.query('DIAG:BGIN:CAT?').split(',')               # HW Catalog
    # for hw in hw_cat:
    #     rdStr = s.query(f'DIAG:BGIN? "{hw}"')
    #     print(f"{hw}: {rdStr}")                                 # HW Config:General

    # #############################################################################
    # ## Extensive Self-Check info
    # #############################################################################
    # testPoints = s.query('DIAG:POIN:CAT?').split(',')           # Retrieve Test points
    # for tp in testPoints:
    #     if 'TEMP' in tp:
    #         rdStr = 'Not Read'
    #     else:
    #         rdStr = s.query(f'DIAG:MEAS:POIN? "{tp}"')
    #     print(f"{tp}: {rdStr}")                                 # HW Config:General
