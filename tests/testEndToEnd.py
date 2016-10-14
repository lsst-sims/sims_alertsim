import unittest
import os
import time
import subprocess
import numpy as np
import lsst.utils.tests
import lsst.sims.alertsim.alertsim_main as alertsim
from lsst.utils import getPackageDir
from lsst.sims.catalogs.db import CatalogDBObject
from lsst.sims.catUtils.mixins import VariabilityStars, PhotometryStars
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.utils import ObservationMetaData
from utils import createFakeOpSimDB, createFakeCatSimDB

def setup_module(module):
    lsst.utils.tests.init()

class AlertSimEndToEndTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scratch_dir = os.path.join(getPackageDir('sims_alertsim'),
                                       'tests', 'scratch')

        pointing_list = ((11.0, -9.0), (145.0, -20.0))

        cls.opsim_file_name = os.path.join(cls.scratch_dir,
                                           'end2end_fake_opsim.db')

        cls.opsim_pointing_list = createFakeOpSimDB(cls.opsim_file_name,
                                                    pointing_list)

        cls.catsim_file_name = os.path.join(cls.scratch_dir,
                                            'end2end_fake_catsim.db')

        createFakeCatSimDB(cls.catsim_file_name,
                           pointing_list)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.opsim_file_name):
            os.unlink(cls.opsim_file_name)

        if os.path.exists(cls.catsim_file_name):
            os.unlink(cls.catsim_file_name)

    def test_alert_sim_end_to_end(self):

        class AlertSimTestCatalogDBObject(CatalogDBObject):

            database = self.catsim_file_name
            driver = 'sqlite'

            objid = 'test_allstars'
            tableid = 'test'
            objectTypeId = 113
            raColName = 'ra'
            decColName = 'decl'
            idColKey = 'id'
            columns = [('raJ2000', 'ra*PI()/180.0'),
                       ('decJ2000', 'decl*PI()/180.0'),
                       ('varParamStr', 'varParamStr', str, 256)]

        class ControlCatalog(VariabilityStars, PhotometryStars, InstanceCatalog):
            column_outputs = ['mjd', 'raJ2000', 'decJ2000', 'mag']
            delimiter = ' '

            transformations = {'raJ2000': np.degrees, 'decJ2000': np.degrees}

            def get_mjd(self):
                return np.array([self.obs_metadata.mjd.TAI]*len(self.column_by_name('raJ2000')))

            def get_galacticAv(self):
                return np.array([0.1]*len(self.column_by_name('raJ2000')))

            def get_mag(self):
                return self.column_by_name('lsst_%s' % self.obs_metadata.bandpass)

        db = AlertSimTestCatalogDBObject()

        cat_name = os.path.join(self.scratch_dir, "end2end_test_cat.txt")
        if os.path.exists(cat_name):
            os.unlink(cat_name)

        for pointing in self.opsim_pointing_list:
            obs = ObservationMetaData(pointingRA=pointing[1],
                                      pointingDec=pointing[2],
                                      mjd=pointing[0],
                                      bandpassName=pointing[3])

            cat = ControlCatalog(db, obs_metadata=obs)

            cat.write_catalog(cat_name, write_mode='a', write_header=False)

        # run alertsim
        # read the control catalog back in
        # compare them


        #receiver_path = os.path.join(getPackageDir('sims_alertsim'),
        #                             "/python/lsst/sims/alertsim/broadcast/receivers/rec_tcp.py")
        receiver_path =  "/Users/danielsf/physics/lsst_160212/Development/sims_alertsim/python/lsst/sims/alertsim/broadcast/receivers/rec_tcp.py"
	command = "python " + receiver_path + " -p 8080"
	subprocess.Popen([command], shell=True)

        time.sleep(5)

        alertsim.main(opsim_table = "",
	    catsim_table = "test_allstars",
            opsim_constraint = "", opsim_path = self.opsim_file_name,
            catsim_constraint = "varParamStr not like 'None'",
            radius = 1.75, protocol = "TcpIp", ipaddr="108.179.167.18",
            port = 8080, header = False, history = False, dia = False)

        filename = os.path.join(dir, "../python/lsst/sims/alertsim/broadcast/receivers/VOEvents.txt")
        voevent_list = read_and_divide(filename)
        ucds = ["pos.eq.ra", "pos.eq.dec", "phot.mag"]
        voevent_data_tuples = parse_parameters(ucds, voevent_list)

	print voevent_data_tuples

        del db
        if os.path.exists(cat_name):
            os.unlink(cat_name)


class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
