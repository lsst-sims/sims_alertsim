""" DiaSourceCommons """
from __future__ import absolute_import
import numpy as np
from .dia_transformations import *
from .random_utils import array_to_dict
from lsst.sims.catalogs.decorators import cached, compound
from lsst.sims.catUtils.mixins import CameraCoords
from lsst.obs.lsstSim import LsstSimMapper

__all__ = ["DiaSourceCommons"]


class DiaSourceCommons(CameraCoords):

    """ Common methods and attributes for all classes 
    which represent diasource.
    Daughter classes will need to override some methods 
    depending of their variability model
    """

    # DIASource columns as of DPDD from May 6th 2016

    
    """
    differences between DPDD and L1 schema
    N = Ndata
    """

    _seed = None
    _rng =None

    column_outputs = ['diaSourceId', 'ccdVisitId',
          'diaObjectId', 'ssObjectId', 'parentDiaSourceId', 'midPointTai',
          'filterName', 'ra', 'decl', 'ra_decl_Cov', 'x','y', 'x_y_Cov', 'apFlux', 
          'apFluxErr', 'snr', 'psFlux', 'psRa','psDecl', 'ps_Cov', 'psLnL', 
          'psChi2', 'psNdata', 'trailFlux', 'trailRa','trailDecl', 'trailLength', 
          'trailAngle', 'trail_Cov', 'trailLnL', 'trailChi2', 'trailNdata', 
          'dipMeanFlux', 'dipFluxDiff', 'dipRa','dipDecl', 'dipLength', 'dipAngle', 
          'dip_Cov', 'dipLnL', 'dipChi2', 'dipNdata', 'totFlux', 'totFluxErr', 
          'diffFlux', 'diffFluxErr', 'fpBkgd', 'fpBkgdErr', 'ixx', 'iyy', 
          'ixy', 'i_cov', 'ixxPSF', 'iyyPSF', 'ixyPSF', 'extendedness',
          'spuriousness', 'flags',]

    # UCD's - Veljko's best guesses. Check this one day please

    ucds = ['meta.id;meta.main', 'meta.id;instr.param',
                'meta.id.assoc', 'meta.id.assoc', 'meta.id.parent',
                'time.epoch', 'instr.filter', 'pos.eq.ra', 'pos.eq.dec',
                'stat.covariance;pos.eq','instr.pixel', 'instr.pixel', 'stat.covariance',
                'phot.flux;arith.diff;phot.calib', 'stat.error;phot.flux', 
                'stat.snr', 'phot.flux;arith.diff', 'pos.eq.ra','pos.eq.dec', 
                'stat.covariance;pos.eq',
                'stat.likelihood;', 'stat.fit.chi2', 'stat.value',
                'phot.flux;arith.diff;phot.calib', 'pos.?','pos.?',
                'stat.likelihood;stat.max', 'stat.likelihood;stat.max',
                'stat.covariance', 'stat.likelihood', 'stat.fit.chi2',
                'stat.value', 'stat.likelihood;stat.max',
                'stat.likelihood;stat.max', 'pos.?','pos.?',
                'stat.likelihood;stat.max', 'stat.likelihood;stat.max',
                'stat.covariance', 'stat.likelihood', 'stat.fit.chi2',
                'stat.value', 'phot.flux;arith.diff;phot.calib',
                'stat.error;phot.flux', 'phot.flux;arith.diff;phot.calib',
                'stat.error;phot.flux', 'pos.cmb', 'stat.error;pos.cmb',
                '', '', '', 'stat.covariance', 'instr.det.psf',
                'instr.det.psf', 'instr.det.psf', '', '', 'meta.code']

    # Datatypes as stated in DPDD

    datatypes = ['uint64', 'uint64', 'uint64',
                'uint64', 'uint64', 'double', 'bit[8]', 'double', 'double', 'float[3]',
                'float', 'float', 'float[3]', 'float', 'float', 'float', 'float',
                'double','double', 'float[6]', 'float', 'float', 'int', 'float',
                'double','double', 'float', 'float', 'float[15]', 'float', 'float',
                'int', 'float', 'float', 'double','double', 'float', 'float',
                'float[15]', 'float', 'float', 'int',  'float', 'float',
                'float', 'float', 'float', 'float', 'float', 'float', 'float',
                'float[6]', 'float', 'float', 'float', 'float', 'float',
                'bit[64]']

    # Units as stated in DPDD

    units = ['', '', '', '', '', 'time', '', 'degrees','degrees',
             'various', 'pixels','pixels', 'various', 'nmgy', 'nmgy', '', 'nmgy',
             'degrees','degrees', 'various', '', '', '', 'nmgy', 'degrees','degrees', 'arcsec',
             'degrees', 'various', '', '', '', 'nmgy', 'nmgy', 'degrees','degrees',
             'arcsec', 'degrees', 'various', '', '', '', 'nmgy', 'nmgy',
             'nmgy', 'nmgy', 'nmgy/asec^2', 'nmgy/asec^2', 'nmgy asec^2',
             'nmgy asec^2', 'nmgy asec^2', 'nmgy^2 asec^4', 'nmgy asec^2',
             'nmgy asec^2', 'nmgy asec^2', '', '', 'bit']

    # DIASource attributes with randomly assigned values (for the time being)

    def write_catalog(self, *args, **kwargs):
        raise NotImplementedError("You cannot call write_catalog() on "
                                  "VariableStarsDia; write_catalog() does not "
                                  "know how to deal with the nested structure "
                                  "of the DIASource schema")

    camera = LsstSimMapper().camera  # the software representation of the LSST camera

    # getters for DIASource attributes which are generated from catsim

    @property
    def rng(self):
        """
        A random number generator for the catalog.
        It is seeded by the self._seed parameter.
        If self._seed is None (default), then rng
        is seeded from the system clock as per numpy's
        default.
        """
        if self._rng is None:
            self._rng = np.random.RandomState(self._seed)
        return self._rng

    def randomFloats(self, n_obj):
        """
        Return a list of random floats between 0 and 1.0
        that is n_obj long.

        If n_obj<0, get n_obj from the length of another
        column in the catalog
        """
        if n_obj < 0:
            n_obj = len(self.column_by_name('chipNum'))

        if n_obj == 0:
            return np.array([])

        return self.rng.random_sample(n_obj)

    def randomFloatArr(self, n_rows, n_cols):
        """
        Return a 2-D array of random floats between 0 and 1.0.
        The array will be n_rows by n_cols.
        If one of the dimensin is less than 0, it will be set
        to the number of rows in the catalog.
        """
        if n_rows < 0:
            n_rows = len(self.column_by_name('chipNum'))
        if n_cols < 0:
            n_cols = len(self.column_by_name('chipNum'))

        if n_cols == 0:
            return np.array([[]]*n_cols)
        if n_rows == 0:
            return np.array([])

        return self.rng.random_sample((n_rows, n_cols)).transpose()

    def randomInts(self, n_obj, i_max=1000):
        """
        Return a list of n_obj random integers between
        zero and i_max (inclusive)

        If n_obj<0, get n_obj from the length of another
        column in the catalog
        """
        if n_obj < 0:
            n_obj = len(self.column_by_name('chipNum'))

        if n_obj == 0:
            return np.array([])
        return self.rng.randint(0,i_max,n_obj)

    def get_parentDiaSourceId(self):
        return self.randomInts(-1, 9223372036854775807)

    def get_psLnL(self):
        return self.randomFloats(-1)

    def get_psChi2(self):
        return self.randomFloats(-1)

    def get_psNdata(self):
        return self.randomInts(-1)

    def get_trailLength(self):
        return self.randomFloats(-1)

    def get_trailAngle(self):
        return self.randomFloats(-1)

    def get_trailLnL(self):
        return self.randomFloats(-1)

    def get_trailChi2(self):
        return self.randomFloats(-1)

    def get_trailNdata(self):
        return self.randomInts(-1)

    def get_dipMeanFlux(self):
        return self.randomFloats(-1)

    def get_dipFluxDiff(self):
        return self.randomFloats(-1)

    def get_dipLength(self):
        return self.randomFloats(-1)

    def get_dipAngle(self):
        return self.randomFloats(-1)

    def get_dipLnL(self):
        return self.randomFloats(-1)

    def get_dipChi2(self):
        return self.randomFloats(-1)

    def get_dipNdata(self):
        return self.randomInts(-1)

    def get_diffFlux(self):
        return self.randomFloats(-1)

    def get_diffFluxErr(self):
        return self.randomFloats(-1)

    def get_fpBkgd(self):
        return self.randomFloats(-1)

    def get_fpBkgdErr(self):
        return self.randomFloats(-1)

    def get_ixx(self):
        return self.randomFloats(-1)

    def get_iyy(self):
        return self.randomFloats(-1)

    def get_ixy(self):
        return self.randomFloats(-1)

    def get_ixxPSF(self):
        return self.randomFloats(-1)

    def get_iyyPSF(self):
        return self.randomFloats(-1)

    def get_ixyPSF(self):
        return self.randomFloats(-1)

    def get_extendedness(self):
        return self.randomFloats(-1)

    def get_spuriousness(self):
        return self.randomFloats(-1)

    def get_flags(self):
        return self.randomInts(-1)

    def get_midPointTai(self):
        """
        Return mid point of exposure 
        """
        return np.array([midPointTai(self.obs_metadata.mjd.TAI)]*len(self.column_by_name('uniqueId')))

    def get_filterName(self):
        return np.array([self.obs_metadata.bandpass]*len(self.column_by_name('uniqueId')))

    @cached
    def get_chipNum(self):
        """
        Concatenate the digits in 'R:i,j S:m,n' to make the chip number ijmn
        """
        return chipNum(self.column_by_name('chipName'))

    def get_ccdVisitId(self):
        """
        Concatenate ObsHistID and chipNum
        """
        return ccdVisitId(self.obs_metadata.OpsimMetaData['obsHistID'], self.column_by_name('chipNum'))

    def get_diaSourceId(self):
        """
        A unique identifier for each DIASource (this needs to be unique for
        each apparition of a given object)
        """
        return diaSourceId(self.column_by_name('uniqueId'), self.obs_metadata.OpsimMetaData['obsHistID'])

    def get_ra(self):
        """
        raICRS takes raJ2000 and add proper motion
        """
        return self.column_by_name('raICRS')


    def get_decl(self):
        """
        decICRS take decJ2000 and add proper motion
        """
        return self.column_by_name('decICRS')

    # DIASource attributes in a form of a list
    # with randomly assigned values (for the time being)

    def get_ra_decl_Cov(self):
        vals = self.randomFloatArr(3, -1)
        cols = ['raSigma', 'declSigma', 'ra_decl_Cov']
        return array_to_dict(cols, vals)


    def get_x(self):
        return self.column_by_name('xPix')

    def get_y(self):
        return self.column_by_name('yPix')
      
    def get_x_y_Cov(self):
        vals = self.randomFloatArr(3, -1)
        cols = ['xSigma', 'ySigma', 'x_y_Cov']
        return array_to_dict(cols, vals)

    @cached
    def get_totMag(self):
        """
        The total magnitude of the variable source (mean + delta)
        """
        return self.column_by_name('lsst_%s' % self.obs_metadata.bandpass)

    @cached
    def get_meanMag(self):
        """
        The mean magnitude of the variable source
        """
        delta_mag = self.column_by_name('delta_lsst_%s' % self.obs_metadata.bandpass)
        tot_mag = self.column_by_name('totMag')
        return tot_mag-delta_mag

    @cached
    def get_totFlux(self):
        """
        The total flux of the variable source
        """
        return fluxFromMag(self.column_by_name('totMag'))

    @cached
    def get_meanFlux(self):
        """
        The mean (quiescent) flux of the variable source
        """
        return fluxFromMag(self.column_by_name('meanMag'))


    @cached
    def get_diaFlux(self):
        """
        Getter for true flux of the source.  Note: this is the flux of the
        difference image: so it is observed flux-mean flux
        """
        return self.column_by_name('totFlux')-self.column_by_name('meanFlux')

    @compound('sigma_meanMag', 'sigma_totMag')
    def get_magUncertainties(self):
        return self._magnitudeUncertaintyGetter(['meanMag', 'totMag'],
                                                [self.obs_metadata.bandpass]*2,
                                                'lsstBandpassDict')

    @compound('diaFluxError', 'totFluxErr', 'meanFluxErr')
    def get_fluxError(self):
        """
        The error in our measurement of the difference image flux.
        """
        mean_mag_error = self.column_by_name('sigma_meanMag')
        tot_mag_error = self.column_by_name('sigma_totMag')
        mean_flux = self.column_by_name('meanFlux')
        tot_flux = self.column_by_name('totFlux')
        return fluxError(mean_mag_error, tot_mag_error, mean_flux, tot_flux)

    @cached
    def get_snr(self):
        """
        Get the SNR
        """
        return snr(self.column_by_name('diaFlux'), self.column_by_name('diaFluxError'))

    def get_psFlux(self):
        """
        Return the true difference image flux plus a small epsilon, since CatSim
        does not have methods to calculate different varieties of flux
        """
        return self.column_by_name('diaFlux') + \
               0.0001*self.randomFloats(-1)

    def get_trailFlux(self):
        """
        Return the true difference image flux plus a small epsilon, since CatSim
        does not have methods to calculate different varieties of flux
        """
        return self.column_by_name('diaFlux') + \
               0.0001*self.randomFloats(-1)

    def get_apFlux(self):
        """
        apMeanSb01 will be the true flux of the source.
        """
        return apFlux(self.column_by_name('diaFlux'))

    def get_apFluxErr(self):
        """
        Calculate the true flux error by getting the magntidue error and assuming that
        magnitude_error = 2.5*log10(1 + 1/SNR)
        """
        return apFluxErr(self.column_by_name('diaFluxError'))
    

    def get_psRa(self):
        """
        Just return raICRS with a small epsilon added, since CatSim does not have methods to calculate psf RA
        """
        return self.column_by_name('raICRS') + 1.0e-6*self.randomFloats(-1)

    def get_psDecl(self):
        """
        Just return decICRS with a small epsilon added, since CatSim does not have methods to calculate psf DEC
        """
        return self.column_by_name('decICRS') + 1.0e-6*self.randomFloats(-1)
      
    def get_ps_Cov(self):
        vals = self.randomFloatArr(6, -1)
        cols = ['psFluxSigma', 'psRaSigma', 'psDeclSigma', 
                'psFlux_psRa_Cov', 'psFlux_psDecl_Cov', 
                'psRa_psDecl_Cov']
        return array_to_dict(cols, vals)

    def get_trailRa(self):
        """
        Just return raICRS with a small epsilon added, since CatSim does not have methods to calculate psf RA
        """
        return self.column_by_name('raICRS') + 1.0e-6*self.randomFloats(-1)

    def get_trailDecl(self):
        """
        Just return decICRS with a small epsilon added, since CatSim does not have methods to calculate psf DEC
        """
        return self.column_by_name('decICRS') + 1.0e-6*self.randomFloats(-1)

    def get_trail_Cov(self):
        vals = self.randomFloatArr(15, -1)
        cols = ['trailFluxSigma', 'trailRaSigma', 'trailDeclSigma', 
                'trailLengthSigma', 'trailAngleSigma', 'trailFlux_trailRa_Cov', 
                'trailFlux_trailDecl_Cov', 'trailFlux_trailLength_Cov', 
                'trailFlux_trailAngle_Cov', 'trailRa_trailDecl_Cov', 
                'trailRa_trailLength_Cov', 'trailRa_trailAngle_Cov', 
                'trailDecl_trailLength_Cov', 'trailDecl_trailAngle_Cov', 
                'trailLength_trailAngle_Cov']
        return array_to_dict(cols, vals)

    def get_dipRa(self):
        """
        Just return raICRS with a small epsilon added, since CatSim does not have methods to calculate psf RA
        """
        return self.column_by_name('raICRS') + 1.0e-6*self.randomFloats(-1)

    def get_dipDecl(self):
        """
        Just return decICRS with a small epsilon added, since CatSim does not have methods to calculate psf DEC
        """
        return self.column_by_name('decICRS') + 1.0e-6*self.randomFloats(-1)

    def get_dip_Cov(self):
        vals = self.randomFloatArr(21, -1)
        cols = ['dipMeanFluxSigma', 'dipFluxDiffSigma', 'dipRaSigma', 
                'dipDeclSigma', 'dipLengthSigma', 'dipAngleSigma', 
                'dipMeanFlux_dipFluxDiff_Cov', 'dipMeanFlux_dipRa_Cov', 
                'dipMeanFlux_dipDecl_Cov', 'dipMeanFlux_dipLength_Cov', 
                'dipMeanFlux_dipAngle_Cov', 'dipFluxDiff_dipRa_Cov', 
                'dipFluxDiff_dipDecl_Cov', 'dipFluxDiff_dipLength_Cov', 
                'dipFluxDiff_dipAngle_Cov', 'dipRa_dipDecl_Cov', 
                'dipRa_dipLength_Cov', 'dipRa_dipAngle_Cov', 'dipDecl_dipLength_Cov', 
                'dipDecl_dipAngle_Cov', 'dipLength_dipAngle_Cov']
        return array_to_dict(cols, vals)

    def get_i_cov(self):
        vals = self.randomFloatArr(6, -1)
        cols = ["ixxSigma", "iyySigma", "ixySigma", 
                "ixx_iyy_Cov", "ixx_ixy_Cov", "iyy_ixy_Cov"]
        return array_to_dict(cols, vals)

    # resolve db column case-sensitivness
    #def get_htmId20(self):
    #    return self._decapitalize_column_name('htmID')

    def _decapitalize_column_name(self, colname):
        if colname in  self.db_obj.columnMap:
            return self.column_by_name(colname)
        else:
            return self.column_by_name(colname.lower())
