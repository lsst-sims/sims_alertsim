from __future__ import with_statement
from builtins import zip
import unittest
import json
import os
import numbers
import tempfile
import shutil
from lsst.utils import getPackageDir
import lsst.utils.tests
from lsst.sims.utils.CodeUtilities import sims_clean_up
from utils import createFakeCatSimDB
from lsst.sims.catUtils.utils import ObservationMetaDataGenerator
from lsst.sims.catalogs.db import CatalogDBObject
from lsst.sims.alertsim.catalogs import DiaSourceVarStars
from lsst.sims.alertsim.jsonConversion import jsonFromCatalog

ROOT = os.path.abspath(os.path.dirname(__file__))

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


def setup_module(module):
    lsst.utils.tests.init()


class JsonTestCase(unittest.TestCase):

    longMessage = True

    @classmethod
    def setUpClass(cls):
        cls.scratch_dir = tempfile.mkdtemp(dir=ROOT, prefix='JsonTestCase-')

        cls.catsim_db_name = os.path.join(cls.scratch_dir,
                                          'json_fake_catsim.db')

        cls.opsim_db = os.path.join(getPackageDir('sims_data'), 'OpSimData',
                                    'opsimblitz1_1133_sqlite.db')

        cls.gen = ObservationMetaDataGenerator(database=cls.opsim_db,
                                               driver='sqlite')

        obs_list = cls.gen.getObservationMetaData(obsHistID=(0,50))
        pointing_list = []
        field_id_list = []
        for obs in obs_list:
            if obs.OpsimMetaData['fieldID'] not in field_id_list:
                field_id_list.append(obs.OpsimMetaData['fieldID'])
                pointing_list.append((obs.pointingRA, obs.pointingDec))

        createFakeCatSimDB(cls.catsim_db_name, pointing_list, n_obj=100,
                           radius=1.75)
        cls.db = LocalStarDB(database=cls.catsim_db_name,
                             host=None, port=None, driver='sqlite')

    @classmethod
    def tearDownClass(cls):
        sims_clean_up()
        del cls.db
        del cls.gen
        if os.path.exists(cls.catsim_db_name):
            os.unlink(cls.catsim_db_name)
        if os.path.exists(cls.scratch_dir):
            shutil.rmtree(cls.scratch_dir)

    def test_diasource_json(self):
        """
        JSONize an instance of DiaSourceVarStars.  Make sure that the
        contents of the resulting text files agree with the contents
        of the catalogs.
        """
        obs_list = self.gen.getObservationMetaData(obsHistID=(0,50))

        json_dir = os.path.join(self.scratch_dir, 'jsonTest')
        if not os.path.exists(json_dir):
            os.mkdir(json_dir)
        else:
            list_of_files = os.listdir(json_dir)
            for file_name in list_of_files:
                os.unlink(os.path.join(json_dir, file_name))

        class testDiaSourceVarStars(DiaSourceVarStars):
            _seed = 44

        jsonFromCatalog(obs_list, testDiaSourceVarStars, self.db, json_dir)

        # read in all of the simulated DIASources written to our json_dir
        list_of_json_files = os.listdir(json_dir)
        dia_dict = {}
        for file_name in list_of_json_files:
            chipNum = int(file_name.split('_')[1])
            full_name = os.path.join(json_dir, file_name)
            with open(full_name, 'r') as input_file:
                list_of_json = input_file.readlines()

            for line in list_of_json:
                source = json.loads(line)
                self.assertIsInstance(source, dict)
                if chipNum not in dia_dict:
                    dia_dict[chipNum] = {}

                diaSourceId = source['diaSourceId']
                dia_dict[chipNum][diaSourceId] = source

        non_random_cols = ['midPointTai', 'filterName', 'ccdVisitId', 'diaSourceId',
                           'ra', 'decl', 'x', 'y', 'totFlux', 'snr']

        unique_chipnum = []
        was_found = {}
        for ix, obs in enumerate(obs_list):
            cat = DiaSourceVarStars(self.db, obs_metadata=obs, column_outputs=['chipNum', 'chipName'])
            cat._seed = 44
            chipNumDex = cat._column_outputs.index('chipNum')
            chipNameDex = cat._column_outputs.index('chipName')
            diaSourceIdDex = cat._column_outputs.index('diaSourceId')
            
            for col in non_random_cols:
                self.assertIn(col, cat._column_outputs)

            comparisons = 0
            for source in cat.iter_catalog():
                chipNum = source[chipNumDex]
                chipName = source[chipNameDex]
                diaSourceId = source[diaSourceIdDex]
                if chipName is not None:
                    if chipNum not in unique_chipnum:
                        unique_chipnum.append(chipNum)
                    control = dia_dict[chipNum][diaSourceId]
                    if chipNum not in was_found:
                        was_found[chipNum] = []

                    # make sure we haven't already discovered this diasource
                    self.assertNotIn(diaSourceId, was_found[chipNum])
                    was_found[chipNum].append(diaSourceId)

                    for ix, (col, val) in enumerate(zip(cat._column_outputs, source)):
                        msg = 'failed on %s' % col
                        if col in non_random_cols:
                            comparisons += 1
                            if isinstance(val, numbers.Number):
                                self.assertAlmostEqual(val, control[col], 10, msg=msg)
                            elif isinstance(val, list):
                                for ix in len(val):
                                    if isinstance(val[ix], numbers.Number):
                                        self.assertAlmostEqual(val[ix], control[col][ix], msg=msg)
                                    else:
                                        self.assertEqual(val[ix], control[col][ix], msg=msg)
                            else:
                                self.assertEqual(val, control[col], msg=msg)

            self.assertGreater(comparisons, 0)
        self.assertGreater(len(unique_chipnum), 1)

        # verify that we found everything we were supposed to
        for chipNum in dia_dict:
            self.assertIn(chipNum, was_found)
            for diaSourceId in dia_dict[chipNum]:
                self.assertIn(diaSourceId, dia_dict[chipNum])
        """
        for file_name in list_of_json_files:
            full_name = os.path.join(json_dir, file_name)
            if os.path.exists(full_name):
                os.unlink(full_name)
        os.rmdir(json_dir)
        """
class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
