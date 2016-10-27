""" DiaSourceCommons """
import numpy as np
import re
from random_utils import *
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catalogs.decorators import cached, compound
from lsst.sims.catUtils.mixins import CameraCoords
from lsst.sims.photUtils import Sed  # for converting magnitudes into fluxes
from lsst.obs.lsstSim import LsstSimMapper
from lsst.sims.catUtils.baseCatalogModels import *
#from lsst.sims.catalogs.decorators import compound

class DiaSourceCommons(CameraCoords):

    """ Common methods and attributes for all classes 
    which represent diasource.
    Daughter classes will need to override some methods 
    depending of their variability model
    """

    # DIASource columns as of DPDD from May 6th 2016

    #column_outputs = VariableStars.column_outputs + ['diaSourceId', 'ccdVisitId',
    
    """
    differences between DPDD and L1 schema
    N = Ndata
    """

    column_outputs = ['diaSourceId', 'ccdVisitId',
          'diaObjectId', 'ssObjectId', 'parentSourceId', 'midPointTai',
          'filterName', 'radec', 'radecCov', 'xy', 'xyCov', 'apFlux', 
          'apFluxErr', 'snr', 'psFlux', 'psRadec', 'psCov', 'psLnL', 
          'psChi2', 'psN', 'trailFlux', 'trailRadec', 'trailLength', 
          'trailAngle', 'trailCov', 'trailLnL', 'trailChi2', 'trailN', 
          'dipMeanFlux', 'dipFluxDiff', 'dipRadec', 'dipLength', 'dipAngle', 
          'dipCov', 'dipLnL', 'dipChi2', 'dipN', 'totFlux', 'totFluxErr', 
          'diffFlux', 'diffFluxErr', 'fpBkgd', 'fpBkgdErr', 'Ixx', 'Iyy', 
          'Ixy', 'Icov', 'IxxPSF', 'IyyPSF', 'IxyPSF', 'extendedness',
          'spuriousness', 'flags',]

    # UCD's - Veljko's best guesses. Check this one day please

    #ucds = VariableStars.ucds + ['meta.id;meta.main', 'meta.id;instr.param',
    ucds = ['meta.id;meta.main', 'meta.id;instr.param',
                'meta.id.assoc', 'meta.id.assoc', 'meta.id.parent',
                'time.epoch', 'instr.filter', 'pos.eq.ra;pos.eq.dec;meta.main',
                'stat.covariance;pos.eq','instr.pixel', 'stat.covariance',
                'phot.flux;arith.diff;phot.calib', 'stat.error;phot.flux', 
                'stat.snr', 'phot.flux;arith.diff', 'pos.eq.ra;pos.eq.dec', 
                'stat.covariance;pos.eq',
                'stat.likelihood;', 'stat.fit.chi2', 'stat.value',
                'phot.flux;arith.diff;phot.calib', 'pos.?',
                'stat.likelihood;stat.max', 'stat.likelihood;stat.max',
                'stat.covariance', 'stat.likelihood', 'stat.fit.chi2',
                'stat.value', 'stat.likelihood;stat.max',
                'stat.likelihood;stat.max', 'pos.?',
                'stat.likelihood;stat.max', 'stat.likelihood;stat.max',
                'stat.covariance', 'stat.likelihood', 'stat.fit.chi2',
                'stat.value', 'phot.flux;arith.diff;phot.calib',
                'stat.error;phot.flux', 'phot.flux;arith.diff;phot.calib',
                'stat.error;phot.flux', 'pos.cmb', 'stat.error;pos.cmb',
                '', '', '', 'stat.covariance', 'instr.det.psf',
                'instr.det.psf', 'instr.det.psf', '', '', 'meta.code']

    # Datatypes as stated in DPDD

    #datatypes = VariableStars.datatypes + ['uint64', 'uint64', 'uint64',
    datatypes = ['uint64', 'uint64', 'uint64',
                'uint64', 'uint64', 'double', 'bit[8]', 'double[2]', 'float[3]',
                'float[2]', 'float[3]', 'float', 'float', 'float', 'float',
                'double[2]', 'float[6]', 'float', 'float', 'int', 'float',
                'double[2]', 'float', 'float', 'float[15]', 'float', 'float',
                'int', 'float', 'float', 'double[2]', 'float', 'float',
                'float[15]', 'float', 'float', 'int',  'float', 'float',
                'float', 'float', 'float', 'float', 'float', 'float', 'float',
                'float[6]', 'float', 'float', 'float', 'float', 'float',
                'bit[64]',]

    # Units as stated in DPDD

    units = ['', '', '', '', '', 'time', '', 'degrees',
             'various', 'pixels', 'various', 'nmgy', 'nmgy', '', 'nmgy',
             'degrees', 'various', '', '', '', 'nmgy', 'degrees', 'arcsec',
             'degrees', 'various', '', '', '', 'nmgy', 'nmgy', 'degrees',
             'arcsec', 'degrees', 'various', '', '', '', 'nmgy', 'nmgy',
             'nmgy', 'nmgy', 'nmgy/asec^2', 'nmgy/asec^2', 'nmgy asec^2',
             'nmgy asec^2', 'nmgy asec^2', 'nmgy^2 asec^4', 'nmgy asec^2',
             'nmgy asec^2', 'nmgy asec^2', '', '', 'bit',]

    # DIASource attributes with randomly assigned values (for the time being)

    default_columns = [('parentSourceId', rbi(), int),
          ('psLnL', rf(), float), ('psChi2', rf(), float),
          ('psN', ri(), int), ('trailLength', rf(), float), ('trailAngle', rf(), float),
          ('trailLnL', rf(), float), ('trailChi2', rf(), float),
          ('trailN', ri(), int), ('dipMeanFlux', rf(), float),
          ('dipFluxDiff', rf(), float), ('dipLength', rf(), float),
          ('dipAngle', rf(), float), ('dipLnL', rf(), float),
          ('dipChi2', rf(), float), ('dipN', ri(), int),
          ('totFlux', rf(), float), ('totFluxErr', rf(), float),
          ('diffFlux', rf(), float), ('diffFluxErr', rf(), float),
          ('fpBkgd', rf(), float), ('fpBkgdErr', rf(), float),
          ('Ixx', rf(), float), ('Iyy', rf(), float), ('Ixy', rf(), float),
          ('IxxPSF', rf(), float), ('IyyPSF', rf(), float),
          ('IxyPSF', rf(), float), ('extendedness', rf(), float),
          ('spuriousness', rf(), float), ('flags', ri(), int)]

    def write_catalog(self, *arks, **kwargs):
        raise NotImplementedError("You cannot call write_catalog() on "
                                  "VariableStarsDia; write_catalog() does not "
                                  "know how to deal with the nested structure "
                                  "of the DIASource schema")

    camera = LsstSimMapper().camera  # the software representation of the LSST camera

    # getters for DIASource attributes which are generated from catsim

    def get_midPointTai(self):
        """
        Return mid point of exposure by taking OpSim start-of-exposure time
        and adding 17 seconds (15 seconds for first exposure; 1 second for
        shutter close; one second for shutter open).  Ignore the fact that,
        as DPDD states, midpoint will vary for different objects based on
        their position relative to the shutter motion.
        """
        return np.array([self.obs_metadata.mjd.TAI+17.0/86400.0]*len(self.column_by_name('uniqueId')))

    def get_filterName(self):
        return np.array([self.obs_metadata.bandpass]*len(self.column_by_name('uniqueId')))

    def get_chipNum(self):
        """
        Concatenate the digits in 'R:i,j S:m,n' to make the chip number ijmn
        """
        chip_name = self.column_by_name('chipName')
        return np.array([int(''.join(re.findall(r'\d+', name))) for name in chip_name])

    def get_ccdVisitId(self):
        """
        Return chipNum*10^7 + obsHistID (obsHistID should never be more than 3 million)
        """
        return self.column_by_name('chipNum')*10000000+self.obs_metadata.OpsimMetaData['obsHistID']

    def get_diaSourceId(self):
        """
        A unique identifier for each DIASource (this needs to be unique for
        each apparition of a given object)

        Take uniqueID, multiply by 10^7 and add obsHistID from self.obs_metadata
        (obsHistID should only go up to about 3 million)
        """
        return self.column_by_name('uniqueId')*10000000+self.obs_metadata.OpsimMetaData['obsHistID']

    def get_radec(self):
        """
        raICRS, decICRS take raJ2000, decJ2000 and
        add proper motion
        """
        ra = self.column_by_name('raICRS')
        dec = self.column_by_name('decICRS')
        vals = np.array([ra, dec]).T
        cols = ['ra', 'dec']
        return array_to_dict(cols, vals)

    # DIASource attributes in a form of a list
    # with randomly assigned values (for the time being)

    def get_radecCov(self):
        vals = np.array(rflist(self, 3)).T
        cols = ['raVar', 'decVar', 'ra_dec_Cov']
        return array_to_dict(cols, vals)


    def get_xy(self):
        vals = np.array([self.column_by_name('xPix'), self.column_by_name('yPix')])
        cols = ['x', 'y']
        return array_to_dict(cols, vals)

    def get_xyCov(self):
        vals = np.array(rflist(self, 3)).T
        cols = ['xVar', 'yVar', 'x_y_Cov']
        return array_to_dict(cols, vals)

    @cached
    def get_trueMag(self):
        """
        The total magnitude of the variable source
        """
        return self.column_by_name('lsst_%s' % self.obs_metadata.bandpass)

    @cached
    def get_meanMag(self):
        """
        The mean magnitude of the variable source
        """
        delta_mag = self.column_by_name('delta_lsst_%s' % self.obs_metadata.bandpass)
        true_mag = self.column_by_name('trueMag')
        return true_mag-delta_mag

    @cached
    def get_totFlux(self):
        """
        The total flux of the variable source
        """
        ss = Sed()
        true_mag = self.column_by_name('trueMag')
        return ss.fluxFromMag(true_mag)

    @cached
    def get_meanFlux(self):
        """
        The mean (quiescent) flux of the variable source
        """
        ss = Sed()
        mean_mag = self.column_by_name('meanMag')
        return ss.fluxFromMag(mean_mag)


    @cached
    def get_trueDiffFlux(self):
        """
        Getter for true flux of the source.  Note: this is the flux of the
        difference image: so it is observed flux-mean flux
        """
        return self.column_by_name('totFlux')-self.column_by_name('meanFlux')

    @compound('trueDiffFluxError', 'totFluxErr', 'meanFluxErr')
    def get_fluxError(self):
        """
        The error in our measurement of the difference image flux.

        Note, we have assumed that

        magnitude_error = 2.5*log10(1 + 1/SNR)

        to get from magnitude errors to SNR
        """
        mag_error = self._magnitudeUncertaintyGetter(['meanMag', 'trueMag'],
                                                     [self.obs_metadata.bandpass]*2,
                                                     'lsstBandpassDict')
        mean_snr = 1.0/(np.power(10.0, mag_error[0]) - 1.0)
        tot_snr = 1.0/(np.power(10.0, mag_error[1]) - 1.0)
        tot_flux_err = self.column_by_name('totFlux')/tot_snr
        mean_flux_err = self.column_by_name('meanFlux')/mean_snr
        return np.array([np.sqrt(tot_flux_err*tot_flux_err + mean_flux_err*mean_flux_err),
                         tot_flux_err, mean_flux_err])

    @cached
    def get_snr(self):
        """
        Get the SNR by dividing flux by uncertainty
        """
        return self.column_by_name('trueDiffFlux')/self.column_by_name('trueDiffFluxError')

    def get_psFlux(self):
        """
        Return the true difference image flux plus a small epsilon, since CatSim
        does not have methods to calculate different varieties of flux
        """
        return self.column_by_name('trueDiffFlux') + \
               0.0001*np.random.random_sample(len(self.column_by_name('uniqueId')))

    def get_trailFlux(self):
        """
        Return the true difference image flux plus a small epsilon, since CatSim
        does not have methods to calculate different varieties of flux
        """
        return self.column_by_name('trueDiffFlux') + \
               0.0001*np.random.random_sample(len(self.column_by_name('uniqueId')))

    def get_apFlux(self):
        """
        apMeanSb01 will be the true flux of the source.

        All others will be apMeanSb01 multiplied by 1.0 + epsilon,
        since CatSim does not contain methods to calculate different
        types of flux.
        """
        true_flux = self.column_by_name('trueDiffFlux')
        vals = np.array([true_flux,
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux))),
                         true_flux*(1.0+0.0001*np.random.random_sample(len(true_flux)))]).T

        cols = ['apMeanSb01', 'apMeanSb02', 'apMeanSb03', 
                 'apMeanSb04', 'apMeanSb05', 'apMeanSb06', 
                 'apMeanSb07', 'apMeanSb08', 'apMeanSb09', 
                 'apMeanSb10']
        return array_to_dict(cols, vals)

    def get_apFluxErr(self):
        """
        Calculate the true flux error by getting the magntidue error and assuming that

        magnitude_error = 2.5*log10(1 + 1/SNR)

        apMeanSb01Sigma will be the true flux error.  Everything else will be true flux error
        multiplied by 1+epsilon because CatSim does not have methods to calculate different types
        of fluxes.
        """
        true_fluxError = self.column_by_name('trueDiffFluxError')

        vals = np.array([true_fluxError,
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError))),
                         true_fluxError*(1.0+0.0001*np.random.random_sample(len(true_fluxError)))]).T

        cols = ['apMeanSb01Sigma', 'apMeanSb02Sigma', 'apMeanSb03Sigma', 
                 'apMeanSb04Sigma', 'apMeanSb05Sigma', 'apMeanSb06Sigma', 
                 'apMeanSb07Sigma', 'apMeanSb08Sigma', 'apMeanSb09Sigma', 
                 'apMeanSb10Sigma']
        return array_to_dict(cols, vals)
    
    def _radec_epsilon(self):
        """
        Return a numpy array of [raICRS+epsilon, decICRS+epsilon].transpose()
        """
        ra = self.column_by_name('raICRS')
        dec = self.column_by_name('decICRS')
        return np.array([ra + 1.0e-6*np.random.random_sample(len(ra)),
                         dec + 1.0e-6*np.random.random_sample(len(dec))]).T

    def get_psRadec(self):
        """
        Just return raICRS, decICRS with a small epsilon added,
        since CatSim does not have methods to calculate psf RA, Dec
        """
        vals = self._radec_epsilon()
        cols = ['psRa', 'psDec']
        return array_to_dict(cols, vals)

    def get_psCov(self):
        vals = np.array(rflist(self, 6)).T
        cols = ['psFluxVar', 'psRaVar', 'psDecVar', 
                'psFlux_psRa_Cov', 'psFlux_psDec_Cov', 
                'psRa_psDec_Cov']
        return array_to_dict(cols, vals)

    def get_trailRadec(self):
        """
        Return raICRS, decICRS with small epsilon, since CatSim
        does not have methods to calculate trailing RA, Dec
        """
        vals = self._radec_epsilon()
        cols = ['trailRa', 'trailDec']
        return array_to_dict(cols, vals)

    def get_trailCov(self):
        vals = np.array(rflist(self, 15)).T
        cols = ['trailFluxVar', 'trailRaVar', 'trailDecVar', 
                'trailLengthVar', 'trailAngleVar', 'trailFlux_trailRa_Cov', 
                'trailFlux_trailDec_Cov', 'trailFlux_trailLength_Cov', 
                'trailFlux_trailAngle_Cov', 'trailRa_trailDec_Cov', 
                'trailRa_trailLength_Cov', 'trailRa_trailAngle_Cov', 
                'trailDec_trailLength_Cov', 'trailDec_trailAngle_Cov', 
                'trailLength_trailAngle_Cov']
        return array_to_dict(cols, vals)

    def get_dipRadec(self):
        """
        Return raICRS, decICRS with small epsilon, since CatSim
        does not have methods to calculate trailing RA, Dec
        """
        vals = self._radec_epsilon()
        cols = ['dipRa', 'dipDec']
        return array_to_dict(cols, vals)

    def get_dipCov(self):
        vals = np.array(rflist(self, 21)).T
        cols = ['dipMeanFluxVar', 'dipFluxDiffVar', 'dipRaVar', 
                'dipDecVar', 'dipLengthVar', 'dipAngleVar', 
                'dipMeanFlux_dipFluxDiff_Cov', 'dipMeanFlux_dipRa_Cov', 
                'dipMeanFlux_dipDec_Cov', 'dipMeanFlux_dipLength_Cov', 
                'dipMeanFlux_dipAngle_Cov', 'dipFluxDiff_dipRa_Cov', 
                'dipFluxDiff_dipDec_Cov', 'dipFluxDiff_dipLength_Cov', 
                'dipFluxDiff_dipAngle_Cov', 'dipRa_dipDec_Cov', 
                'dipRa_dipLength_Cov', 'dipRa_dipAngle_Cov', 'dipDec_dipLength_Cov', 
                'dipDec_dipAngle_Cov', 'dipLength_dipAngle_Cov']
        return array_to_dict(cols, vals)

    def get_Icov(self):
        vals = np.array(rflist(self, 6)).T
        cols = ["IxxVar", "IyyVar", "IxyVar", 
                "Ixx_Iyy_Cov", "Ixx_Ixy_Cov", "Iyy_Ixy_Cov"]
        return array_to_dict(cols, vals)

    # resolve db column case-sensitivness
    #def get_htmId20(self):
    #    return self._decapitalize_column_name('htmID')

    def _decapitalize_column_name(self, colname):
        if colname in  self.db_obj.columnMap.keys():
            return self.column_by_name(colname)
        else:
            return self.column_by_name(colname.lower())
