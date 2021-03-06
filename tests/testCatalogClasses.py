from __future__ import with_statement
import unittest
import os
import tempfile
import shutil
import lsst.utils.tests
from lsst.utils import getPackageDir
from utils import createFakeCatSimDB
from lsst.sims.utils.CodeUtilities import sims_clean_up
from lsst.sims.utils import ObservationMetaData
from lsst.sims.catUtils.utils import ObservationMetaDataGenerator
from lsst.sims.catalogs.db import CatalogDBObject
from lsst.sims.alertsim.catalogs import BasicVarStars, DiaSourceVarStars

ROOT = os.path.abspath(os.path.dirname(__file__))


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
               ('sedFilename', 'sedfilename', str, 40)]


class AlertSimCatalogTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scratch_dir = tempfile.mkdtemp(dir=ROOT, prefix='AlertSimCatalogTestCase-')
        cls.db_file_name = os.path.join(cls.scratch_dir, "catalog_test_obj.db")

        opsim_db = os.path.join(getPackageDir("sims_data"), "OpSimData", "opsimblitz1_1133_sqlite.db")
        gen = ObservationMetaDataGenerator(database=opsim_db, driver='sqlite')
        obs_list = gen.getObservationMetaData(night=3)
        cls.obs = obs_list[0]

        cls.control_stars = createFakeCatSimDB(cls.db_file_name,
                                               [(cls.obs.pointingRA, cls.obs.pointingDec)])

        cls.db = LocalStarDB(database=cls.db_file_name, host=None, port=None,
                             driver='sqlite')

    @classmethod
    def tearDownClass(cls):
        sims_clean_up()
        del cls.db
        if os.path.exists(cls.db_file_name):
            os.unlink(cls.db_file_name)
        if os.path.exists(cls.scratch_dir):
            shutil.rmtree(cls.scratch_dir)

    def testBasicVarStars(self):
        """
        Just test that the BasicVarStars catalog runs
        """
        cat = BasicVarStars(self.db, obs_metadata=self.obs)

        with lsst.utils.tests.getTempFilePath('.txt') as cat_name:
            cat.write_catalog(cat_name)
            with open(cat_name, 'r') as input_file:
                lines = input_file.readlines()
            self.assertGreater(len(lines), 1)

    def test_variable_stars_dia(self):
        """
        Just test that the VariableStarsDia catalog runs
        """
        cat = DiaSourceVarStars(self.db, obs_metadata=self.obs)

        # You cannot write a VariableStarsDia catalog, but you can iterate
        # over it.  Test that iter_catalog() works but that write_catalog()
        # raises a NotImplementedError
        ct = 0
        for line in cat.iter_catalog():
            ct += 1
        self.assertGreater(ct, 1)

        cat_name = os.path.join(self.scratch_dir, "variable_stars_dia_test_output.txt")

        with self.assertRaises(NotImplementedError):
            cat.write_catalog(cat_name)

        if os.path.exists(cat_name):
            os.unlink(cat_name)


class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
