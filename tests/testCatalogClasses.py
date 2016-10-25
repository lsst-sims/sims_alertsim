from __future__ import with_statement
import unittest
import os
import lsst.utils.tests
from lsst.utils import getPackageDir
from utils import createFakeCatSimDB
from lsst.sims.utils import ObservationMetaData
from lsst.sims.catalogs.db import CatalogDBObject
from lsst.sims.alertsim.catalogs import VariableStars


def setup_module(module):
    lsst.utils.tests.init()


class LocalStarDB(CatalogDBObject):
    tableid = 'test'
    idColKey = 'id'
    raColName = 'ra'
    decColName = 'decl'
    objectTypeId = 15

    columns = [('simobjid', 'id', int),
               ('raJ2000', 'ra*PI()/180.'),
               ('decJ2000', 'decl*PI()/180.'),
               ('glon', 'gal_l*PI()/180.'),
               ('glat', 'gal_b*PI()/180.'),
               ('properMotionRa', '(mura/(1000.*3600.))*PI()/180.'),
               ('properMotionDec', '(mudecl/(1000.*3600.))*PI()/180.'),
               ('parallax', 'parallax*PI()/648000000.'),
               ('galacticAv', 'ebv*3.1'),
               ('radialVelocity', 'vrad'),
               ('variabilityParameters', 'varParamStr', str, 256),
               ('sedFilename', 'sedfilename', unicode, 40)]


class AlertSimCatalogTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_file_name = os.path.join(getPackageDir("sims_alertsim"),
                                        "tests", "scratch", "catalog_test_obj.db")

        cls.obs = ObservationMetaData(pointingRA=23.0, pointingDec=-17.0,
                                      mjd=60000.0, rotSkyPos=19.0,
                                      boundType='circle', boundLength=1.75)

        cls.control_stars = createFakeCatSimDB(cls.db_file_name,
                                               [(cls.obs.pointingRA, cls.obs.pointingDec)])

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_file_name):
            os.unlink(cls.db_file_name)

    def testVariableStars(self):
        """
        Just test that the VariableStars catalog runs
        """
        db = LocalStarDB(database=self.db_file_name, host=None, port=None,
                         driver='sqlite')

        cat = VariableStars(db, obs_metadata=self.obs)
        cat_name = os.path.join(getPackageDir("sims_alertsim"),
                                "tests", "scratch", "variable_stars_test_output.txt")

        if os.path.exists(cat_name):
            os.unlink(cat_name)

        cat.write_catalog(cat_name)
        with open(cat_name, 'r') as input_file:
            lines = input_file.readlines()
            self.assertGreater(lines, 1)

        if os.path.exists(cat_name):
            os.unlink(cat_name)


class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
