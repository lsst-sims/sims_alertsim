from __future__ import with_statement
import numpy as np
import os
import json

from lsst.utils import getPackageDir
from lsst.sims.catalogs.db import fileDBObject
from lsst.sims.utils import _galacticFromEquatorial

__all__ = ["createFakeOpSimDB", "createFakeCatSimDB"]


def createFakeOpSimDB(file_name, pointing_list):
    """
    Creates a fake OpSim database (i.e. a sqlite database with a Summary
    table that has the same schema as OpSim).

    file_name will be the name of the file created.
    pointing_list is a list of (ra, dec) positions at which to point.

    Will output a list of (MJD, RA, Dec, filter) corresponding to the
    observations contained.
    """

    if os.path.exists(file_name):
        os.unlink(file_name)

    output_list = []

    rng = np.random.RandomState(119)
    bandpass_list = np.array(['g', 'r', 'i'])
    n_obs = 5

    scratch_dir = os.path.join(getPackageDir('sims_alertsim'),
                               'tests', 'scratch')

    scratch_file_name = os.path.join(scratch_dir, '%s.dat' % file_name)

    if os.path.exists(scratch_file_name):
        os.unlink(scratch_file_name)

    obshistid = 0
    with open(scratch_file_name, 'w') as output_file:
        output_file.write('# mjd ra dec filter\n')
        for i_p, pointing in enumerate(pointing_list):
            ra = np.radians(pointing[0])
            dec = np.radians(pointing[1])
            mjd_list = rng.random_sample(n_obs)*3653.0 + 59580.0

            bandpass_dex_list = rng.random_integers(0, 2, n_obs)
            for mjd, bandpass in zip(mjd_list, bandpass_list[bandpass_dex_list]):
                night = int(round(mjd-59580.0))
                obshistid += 1
                output_file.write('%.6f %.6f %.6f %s 23.0 0.7 %d %d %d\n' %
                                 (mjd, ra, dec, bandpass, i_p, night, obshistid))
                output_list.append((mjd, ra, dec, bandpass))

    dtype = np.dtype([('expMJD', float), ('fieldRA', float), ('fieldDec', float),
                      ('filter', str, 1), ('fiveSigmaDepth', float), ('rawSeeing', float),
                      ('fieldID', int), ('night', int), ('obsHistID', int)])

    fileDBObject(scratch_file_name, runtable='Summary', database=file_name,
                 dtype=dtype, delimiter=' ', idColKey='expMJD')

    os.unlink(scratch_file_name)

    return output_list


def createFakeCatSimDB(file_name, pointing_list):
    """
    Creates a sqlite database with a CatSim-like schema.
    The database will be populated with a handful of RRLyrae for alertsim testing.

    file_name is the name of the file to be created
    pointing_list is a list of (ra, dec) tuples corresponding to the pointings to be populated

    will return a listof (RA, Dec, sed, magNorm, EBV, varParamStr)
    """

    scratch_dir = os.path.join(getPackageDir('sims_alertsim'), 'tests', 'scratch')
    sed_dir = os.path.join(getPackageDir('sims_sed_library'), 'starSED', 'kurucz')
    sed_list = np.array(os.listdir(sed_dir))

    lc_subdir = os.path.join('rrly_lc', 'RRab')
    lc_dir = os.path.join(getPackageDir('sims_sed_library'), lc_subdir)
    lc_list = np.array(os.listdir(lc_dir))

    if os.path.exists(file_name):
        os.unlink(file_name)

    n_obj = 3

    rng = np.random.RandomState(771)

    dtype = np.dtype([('id', int), ('ra', float), ('decl', float),
                      ('sedFilename', str, 100), ('magNorm', float),
                      ('ebv', float), ('varParamStr', str, 256),
                      ('parallax', float), ('mura', float), ('mudecl', float),
                      ('vrad', float), ('galacticAv', float), ('gal_l', float),
                      ('gal_b', float)])

    scratch_file_name = os.path.join(scratch_dir, '%s.dat' % file_name)
    if os.path.exists(scratch_file_name):
        os.unlink(scratch_file_name)

    ct = 1
    with open(scratch_file_name, 'w') as output_file:
        output_file.write("# a header\n")
        for pointing in pointing_list:
            rr = rng.random_sample(n_obj)*0.1
            theta = rng.random_sample(n_obj)*2.0*np.pi
            ra_list = pointing[0] + rr*np.cos(theta)
            dec_list = pointing[1] + rr*np.sin(theta)
            sed_dex_list = rng.random_integers(0, len(sed_list)-1, n_obj)
            ebv_list = 0.1 + rng.random_sample(n_obj)*0.5
            lc_dex_list = rng.random_integers(0, len(lc_list)-1, n_obj)
            magnorm_list = rng.random_sample(n_obj)*5.0+15.0
            gal_l_list, gal_b_list = _galacticFromEquatorial(np.radians(ra_list),
                                                             np.radians(dec_list))

            for ra, dec, magnorm, sed, ebv, lc, gal_l, gal_b in \
                zip(ra_list, dec_list, magnorm_list, sed_list[sed_dex_list],
                    ebv_list, lc_list[lc_dex_list], gal_l_list, gal_b_list):

                varParamDict = {'varMethodName': 'applyRRly',
                                'pars': {'filename': os.path.join(lc_subdir, lc),
                                         'tStartMjd': 59579.0}}

                varParamStr = json.dumps(varParamDict)

                output_file.write("%d;%.6f;%.6f;%s;%.6f;%.6f;%s;0.0;0.0;0.0;0.0;0.1;%.6f;%.6f\n" %
                                  (ct, ra, dec, sed, magnorm, ebv, varParamStr, gal_l, gal_b))
                ct += 1

    fileDBObject(scratch_file_name, runtable='test', database=file_name,
                 dtype=dtype, delimiter=';', idColKey='id')

    if os.path.exists(scratch_file_name):
        os.unlink(scratch_file_name)
