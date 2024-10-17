import unittest
from common import NilanProxyCTS602, NilanProxyDatapointKey
from modelTester import modelTester

class CTS602WithNoQuirksTest(modelTester):    
    def setUp(self):
        self.loadedModel = NilanProxyCTS602()
        self.loadedModel.add_device_quirks(0,0,0) # Should not load any quirks.
        self.expectedName = "CTS 602"
        self.expectedManufacturer = "Nilan"

    def test_quirks_not_loaded(self):
        self.assertNotIn(NilanProxyDatapointKey.TEMP_HOTWATER_TOP, self.loadedModel.datapoints)

class CTS602WithQuirksTest(modelTester):    
    def setUp(self):
        self.loadedModel = NilanProxyCTS602()
        self.loadedModel.add_device_quirks(0,0,12)
        self.expectedName = "CTS 602"
        self.expectedManufacturer = "Nilan"

    def test_hotwater_temp_quirk_loaded(self):
        self.assertIn(NilanProxyDatapointKey.TEMP_HOTWATER_TOP, self.loadedModel.datapoints)
    

if __name__ == '__main__':
    unittest.main()