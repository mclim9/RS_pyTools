from iSocket import iSocket                             # Import socket module
from VSA_K18_Speed import System_Init, K18_Apply_MM, K18_Calc_DPD, K18_Short_Capture
from VSG_K144_Waveform_Creation import SMW_Load_Arb, SMW_Get_Dir

if __name__ == '__main__':
    global FSW, SMW
    FSW = iSocket().open('192.168.58.109', 5025)
    SMW = iSocket().open('192.168.58.114', 5025)
    FSW.timeout(5)                                          # Timeout in seconds

    filelist = SMW_Get_Dir(SMW, '//var//user//ML_Data')
    for TMFile in filelist:
        SMW_Load_Arb(SMW, TMFile)
        System_Init(FSW, SMW)
        K18_Short_Capture(FSW)
    # K18_Calc_DPD()
    # K18_Apply_MM()
    # NR5G_Config()
    # NR5G_EVM()
