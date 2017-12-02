import unittest
import os
import copy
import numpy as np
import lsst.utils.tests
from lsst.utils import getPackageDir
from lsst.sims.alertsim.opsim_utils import _convert_obs_to_history
from lsst.sims.catUtils.utils import ObservationMetaDataGenerator


def setup_module(module):
    lsst.utils.tests.init()


class ObsHistoryTestCase(unittest.TestCase):

    longMessage = True

    def test_history(self):
        """
        Test that _convert_obs_to_history really does sort the
        ObservationMetaData appropriately.
        """

        opsimdb = os.path.join(getPackageDir("sims_data"), "OpSimData",
                               "opsimblitz1_1133_sqlite.db")

        gen = ObservationMetaDataGenerator(opsimdb)
        obs_list = gen.getObservationMetaData(night=(0,10))
        obs_control = copy.deepcopy(obs_list)
        control_fieldid = np.array([obs.OpsimMetaData['fieldID'] for obs in obs_control])
        control_mjd = np.array([obs.mjd.TAI for obs in obs_control])
        self.assertGreater(len(obs_list), 1)

        history = _convert_obs_to_history(obs_list, gen)

        for ix, entry in enumerate(history):

            # make sure that the leading ObservationMetaData in each
            # row of history is at a later date than the leading
            # ObservationMetaData of the preceding entry
            if ix > 0:
                msg = 'offending index is %d' % ix
                self.assertGreater(entry[0].mjd.TAI, history[ix-1][0].mjd.TAI, msg=msg)

            # Make sure that the ObservationMetaData in each entry are in
            # reverse chronological order and unique
            obshistid_list = []
            for iy, past_obs in enumerate(entry):
                self.assertNotIn(past_obs.OpsimMetaData['obsHistID'], obshistid_list)
                obshistid_list.append(past_obs.OpsimMetaData['obsHistID'])

                self.assertEqual(past_obs.OpsimMetaData['fieldID'],
                                 entry[0].OpsimMetaData['fieldID'])
                if iy > 0:
                    msg = 'offending index is %d' % iy
                    self.assertLess(past_obs.mjd.TAI, entry[iy-1].mjd.TAI, msg=msg)

            # Make sure that every ObservationMetaData that should be in this entry
            # in the history is in this entry in the history
            obshistid_list = [obs.OpsimMetaData['obsHistID'] for obs in entry]
            should_be_in = np.where(np.logical_and(control_mjd <= entry[0].mjd.TAI,
                                                   control_fieldid == entry[0].OpsimMetaData['fieldID']))[0]

            for shld_dex in should_be_in:
                self.assertIn(obs_control[shld_dex].OpsimMetaData['obsHistID'], obshistid_list)


class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
