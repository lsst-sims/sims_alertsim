import unittest
import lsst.utils.tests

def setup_module(module):
    lsst.utils.tests.init()

class AlertSimEndToEndTest(unittest.TestCase):
    pass



class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass

if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
