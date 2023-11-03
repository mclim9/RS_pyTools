from unittest               import TestCase
# import sys
from pyTools.mock.iSocket   import iSocket           # mock socket


class TestGeneral(TestCase):
    def setUp(self):                                # Run before each test
        # sys.path.append('../pyTools')
        print("", end="")

    def tearDown(self):                             # Run after each test
        pass

    def test_main(self):
        from pyTools.RTP.iSck_RTP_Get_Meas          import main
        main.iSocket = iSocket()
        main.main()
