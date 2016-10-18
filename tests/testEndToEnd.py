import unittest
import os
import sys
import time
import subprocess
import socket
import numpy as np
import lsst.utils.tests
import lsst.sims.alertsim.alertsim_main as alertsim
from lsst.utils import getPackageDir
from lsst.sims.catalogs.db import CatalogDBObject
from lsst.sims.catUtils.mixins import VariabilityStars, PhotometryStars
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.utils import ObservationMetaData
from utils import createFakeOpSimDB, createFakeCatSimDB

from receiver_parser import read_and_divide, parse_parameters

from astropy.time import Time

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
            obs = ObservationMetaData(pointingRA=np.degrees(pointing[1]),
                                      pointingDec=np.degrees(pointing[2]),
                                      mjd=pointing[0],
                                      bandpassName=pointing[3],
                                      boundLength=1.75,
                                      boundType='circle')

            cat = ControlCatalog(db, obs_metadata=obs)

            cat.write_catalog(cat_name, write_mode='a', write_header=False)

        # run alertsim
        # read the control catalog back in
        # compare them

        #current path
        dir_path = os.path.dirname(os.path.realpath(__file__))

        #combine parent path with receiver path
        receiver_path = os.path.dirname(dir_path) + "/python/lsst/sims/alertsim/broadcast/receivers/rec_tcp.py"

        #shell command for a receiver to be executed in a different process
        command = "python " + receiver_path + " -p 8080"
        subprocess.Popen([command], shell=True)

        #wait a bit till receiver warms up
        time.sleep(5)

        #retreive local ipaddress
        local_ip_adress = "127.0.0.1"

        #works on mac
        if sys.platform == 'darwin':
            local_ip_address = socket.gethostbyname(socket.gethostname())
        else:
        #works on linux, at least OpenSuSE
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
            local_ip_address = s.getsockname()[0]

        alertsim.main(opsim_table = "",
	    catsim_table = "test_allstars",
            opsim_constraint = "", opsim_path = self.opsim_file_name,
            catsim_constraint = "varParamStr not like 'None'",
            radius = 1.75, protocol = "TcpIp", ipaddr=local_ip_address,
            port = 8080, header = False, history = False, dia = False)

        filename = "VOEvents.txt"
        voevent_list = read_and_divide(filename)

        ucds = ["pos.eq.ra", "pos.eq.dec", "phot.mag"]
        voevent_data_tuples = parse_parameters(ucds, voevent_list)

	print voevent_data_tuples

        dtype = np.dtype([('mjd', float), ('ra', float), ('dec', float),
                          ('mag', float)])
        control_data = np.genfromtxt(cat_name, dtype=dtype)

        # check that the number of voevents matches
        # the number of rows in our test column
        self.assertEqual(len(control_data), len(voevent_data_tuples),
                         msg=('%d catalog entries; %d voevents'
                              % (len(control_data), len(voevent_data_tuples))))

        # loop over voevents, verifying that each one agrees with
        # the contents of the catalog
        tol = 1.0e-7
        for event in voevent_data_tuples:
            date = Time(event[4], scale='tai', format='isot')
            tai = data.tai.mjd
            ix = np.argmin(np.abs(tai-control_data['mjd']))
            catobj = control_data[ix]
            self.assertLess(np.abs(tai-catobj['mjd']), tol)
            self.assertLess(np.abs(np.degrees(event[0])-catobj['ra']), tol)
            self.assertLess(np.abs(np.degrees(event[1])-catobj['dec']), tol)
            self.assertLess(np.abs(event[2]-cataobj['mag']), tol)

        del db
        if os.path.exists(cat_name):
            os.unlink(cat_name)


class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
