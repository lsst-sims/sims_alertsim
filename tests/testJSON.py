from __future__ import with_statement
import unittest
import json
import os
import numbers
from lsst.utils import getPackageDir
import lsst.utils.tests
from utils import createFakeCatSimDB
from lsst.sims.catUtils.utils import ObservationMetaDataGenerator
from lsst.sims.catalogs.db import CatalogDBObject
from lsst.sims.alertsim.catalogs import DiaSourceVarStars
from lsst.sims.alertsim.json_utils import jsonFromCatalog


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


def setup_module(module):
    lsst.utils.tests.init()


class JsonTestCase(unittest.TestCase):

    longMessage = True

    @classmethod
    def setUpClass(cls):
        cls.scratch_dir = os.path.join(getPackageDir('sims_alertsim'),
                                      'tests', 'scratch')

        cls.catsim_db_name = os.path.join(cls.scratch_dir,
                                          'json_fake_catsim.db')

        if os.path.exists(cls.catsim_db_name):
            os.unlink(cls.catsim_db_name)

        cls.opsim_db = os.path.join(getPackageDir('sims_data'), 'OpSimData',
                                    'opsimblitz1_1133_sqlite.db')

        cls.gen = ObservationMetaDataGenerator(database=cls.opsim_db,
                                               driver='sqlite')

        obs_list = cls.gen.getObservationMetaData(night=(0,2))
        pointing_list = []
        field_id_list = []
        for obs in obs_list:
            if obs.OpsimMetaData['fieldID'] not in field_id_list:
                field_id_list.append(obs.OpsimMetaData['fieldID'])
                pointing_list.append((obs.pointingRA, obs.pointingDec))

        createFakeCatSimDB(cls.catsim_db_name, pointing_list)
        cls.db = LocalStarDB(database=cls.catsim_db_name,
                             host=None, port=None, driver='sqlite')

    @classmethod
    def tearDownClass(cls):
        del cls.db
        del cls.gen
        if os.path.exists(cls.catsim_db_name):
            os.unlink(cls.catsim_db_name)

    def test_diasource_json(self):
        """
        JSONize an instance of DiaSourceVarStars.  Make sure that the
        contents of the resulting text files agree with the contents
        of the catalogs.
        """
        obs_list = self.gen.getObservationMetaData(obsHistID=(0,50))

        json_dir = os.path.join(getPackageDir('sims_alertsim'),
                                'tests', 'scratch', 'jsonTest')
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

        for ix, obs in enumerate(obs_list):
            cat = DiaSourceVarStars(self.db, obs_metadata=obs, column_outputs=['chipNum'])
            cat._seed = 44
            chipNumDex = cat._column_outputs.index('chipNum')
            diaSourceIdDex = cat._column_outputs.index('diaSourceId')

            for source in cat.iter_catalog():
                chipNum = source[chipNumDex]
                diaSourceId = source[diaSourceIdDex]

                control = dia_dict[chipNum][diaSourceId]
                comparisons = 0
                for ix, (col, val) in enumerate(zip(cat._column_outputs, source)):
                    msg = 'failed on %s' % col
                    if col != 'chipNum':
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

        for file_name in list_of_json_files:
            full_name = os.path.join(json_dir, file_name)
            if os.path.exists(full_name):
                os.unlink(full_name)
        os.rmdir(json_dir)

class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()

