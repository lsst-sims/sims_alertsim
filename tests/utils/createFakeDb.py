from __future__ import with_statement
import numpy as np
import os

from lsst.utils import getPackageDir
from lsst.sims.catalogs.db import fileDBObject

__all__ = ["createFakeOpSimDB"]


def createFakeOpSimDB(file_name):
    """
    Creates a fake OpSim database (i.e. a sqlite database with a Summary
    table that has the same schema as OpSim).

    file_name will be the name of the file created.

    Will output a list of (MJD, RA, Dec, filter) corresponding to the
    observations contained.
    """

    if os.path.exists(file_name):
        os.unlink(file_name)

    output_list = []

    rng = np.random.RandomState(119)
    bandpass_list = np.array(['g', 'r', 'i'])
    n_obs = 25

    scratch_dir = os.path.join(getPackageDir('sims_alertsim'),
                               'tests', 'scratch')

    scratch_file_name = os.path.join(scratch_dir, '%s.dat' % file_name)

    if os.path.exists(scratch_file_name):
        os.unlink(scratch_file_name)

    with open(scratch_file_name, 'w') as output_file:
        output_file.write('# mjd ra dec filter\n')
        for ra, dec in zip((45.0, 100.0), (-11.0, -20.0)):
            mjd_list = rng.random_sample(n_obs)*3653.0 + 59580.0

            bandpass_dex_list = rng.random_integers(0, 2, n_obs)
            for mjd, bandpass in zip(mjd_list, bandpass_list[bandpass_dex_list]):
                output_file.write('%.6f %.6f %.6f %s\n' % (mjd, ra, dec, bandpass))
                output_list.append((mjd, ra, dec, bandpass))

    dtype = np.dtype([('expMJD', float), ('fieldRA', float), ('fieldDec', float),
                      ('filter', str, 1)])

    fileDBObject(scratch_file_name, runtable='Summary', database=file_name,
                 dtype=dtype, delimiter=' ', idColKey='expMJD')

    os.unlink(scratch_file_name)

    return output_list
