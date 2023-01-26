from iSocket import iSocket                 # Import socket module


    def apply_user_correction(self, source, destination):
        self.write_file(source, destination)
        self.operation_complete()
        # self._resource.write(":SENS:CORR:FRES:USER:SLIS1:REM")
        # self._resource.write('CORR:FRES:USER:SLIS1:SEL "C:\\R_S\\instr\\user\\ideal_attenuator_10dB.s2p"')
        self._resource.write('CORR:FRES:USER:SLIS1:SEL "{}"'.format(destination))
        self._resource.write(":SENS:CORR:FRES:USER:SCOP ALL")                   # Apply to ALL
        self._resource.query(":SENS:CORR:FRES:USER:STAT ON;*OPC?")              # K544 ON
        self._resource.query(':SENS:CORR:FRES:INP:USER:SLIS1:STAT OFF;*OPC?')
        self._resource.query(':SENS:CORR:FRES:INP:USER:SLIS1:STAT ON;*OPC?')


if __name__ == "__main__":
    s      = iSocket().open('192.168.58.109', 5025)