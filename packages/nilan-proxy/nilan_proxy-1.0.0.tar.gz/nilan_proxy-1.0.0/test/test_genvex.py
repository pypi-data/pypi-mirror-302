import unittest
from common import NilanProxyOptima250, NilanProxyOptima251, NilanProxyOptima260, NilanProxyOptima270, NilanProxyOptima301, NilanProxyOptima312, NilanProxyOptima314
from modelTester import modelTester

class Optima250Test(modelTester):    
    def setUp(self):
        self.loadedModel = NilanProxyOptima250()
        self.expectedName = "Optima 250"
        self.expectedManufacturer = "Genvex"

class Optima251Test(modelTester):    
    def setUp(self):
        self.loadedModel = NilanProxyOptima251()
        self.expectedName = "Optima 251"
        self.expectedManufacturer = "Genvex"

class Optima260Test(modelTester):
    def setUp(self):
        self.loadedModel = NilanProxyOptima260()
        self.expectedName = "Optima 260"
        self.expectedManufacturer = "Genvex"

class Optima270Test(modelTester):
    def setUp(self):
        self.loadedModel = NilanProxyOptima270()
        self.expectedName = "Optima 270"
        self.expectedManufacturer = "Genvex"

class Optima301Test(modelTester):
    def setUp(self):
        self.loadedModel = NilanProxyOptima301()
        self.expectedName = "Optima 301"
        self.expectedManufacturer = "Genvex"

class Optima312Test(modelTester):
    def setUp(self):
        self.loadedModel = NilanProxyOptima312()
        self.expectedName = "Optima 312"
        self.expectedManufacturer = "Genvex"

class Optima314Test(modelTester):
    def setUp(self):
        self.loadedModel = NilanProxyOptima314()
        self.expectedName = "Optima 314"
        self.expectedManufacturer = "Genvex"

if __name__ == '__main__':
    unittest.main()