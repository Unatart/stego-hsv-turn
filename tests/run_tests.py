import unittest
from tests.integration_steg import IntegrationStegano
from tests.system_steg import SystemManager
from tests.unit_steg import UnitAES, UnitTSS

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestSuite((
        unittest.makeSuite(UnitAES),
        unittest.makeSuite(UnitTSS),
        unittest.makeSuite(SystemManager),
        unittest.makeSuite(IntegrationStegano)
    )))