""" DiaSourceCommons """
import numpy as np
from random_utils import *
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catUtils.baseCatalogModels import *
#from lsst.sims.catalogs.decorators import compound

class DiaSourceCommons(InstanceCatalog):

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

    default_columns = [('ccdVisitId', rbi(), int),
          ('diaObjectId', rbi(), int), ('ssObjectId', rbi(), int),
          ('parentSourceId', rbi(), int), ('midPointTai', rf(), float),
          ('filterName', 0, (str, 8)),
          ('snr', rf(), float), ('psFlux', rf(), float),
          ('psLnL', rf(), float), ('psChi2', rf(), float),
          ('psN', ri(), int), ('trailFlux', rf(), float),
          ('trailLength', rf(), float), ('trailAngle', rf(), float),
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

    # getters for DIASource attributes which are generated from catsim

    def get_diaSourceId(self):
        """
        A unique identifier for each DIASource (this needs to be unique for
        each apparition of a given object)
        """
        return self.column_by_name('simobjid')

    def get_radec(self):
        ra = self.column_by_name('raJ2000')
        dec = self.column_by_name('decJ2000')
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
        vals = np.array(rflist(self, 2)).T
        cols = ['x', 'y']
        return array_to_dict(cols, vals)

    def get_xyCov(self):
        vals = np.array(rflist(self, 3)).T
        cols = ['xVar', 'yVar', 'x_y_Cov']
        return array_to_dict(cols, vals)

    def get_apFlux(self):
        vals = np.array(rflist(self, 10)).T
        cols = ['apMeanSb01', 'apMeanSb02', 'apMeanSb03', 
                 'apMeanSb04', 'apMeanSb05', 'apMeanSb06', 
                 'apMeanSb07', 'apMeanSb08', 'apMeanSb09', 
                 'apMeanSb10']
        return array_to_dict(cols, vals)

    def get_apFluxErr(self):
        vals = np.array(rflist(self, 10)).T
        cols = ['apMeanSb01Sigma', 'apMeanSb02Sigma', 'apMeanSb03Sigma', 
                 'apMeanSb04Sigma', 'apMeanSb05Sigma', 'apMeanSb06Sigma', 
                 'apMeanSb07Sigma', 'apMeanSb08Sigma', 'apMeanSb09Sigma', 
                 'apMeanSb10Sigma']
        return array_to_dict(cols, vals)
    
    def get_psRadec(self):
        vals = np.array(rflist(self, 2)).T
        cols = ['psRa', 'psDec']
        return array_to_dict(cols, vals)

    def get_psCov(self):
        vals = np.array(rflist(self, 6)).T
        cols = ['psFluxVar', 'psRaVar', 'psDecVar', 
                'psFlux_psRa_Cov', 'psFlux_psDec_Cov', 
                'psRa_psDec_Cov']
        return array_to_dict(cols, vals)

    def get_trailRadec(self):
        vals = np.array(rflist(self, 2)).T
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
        vals = np.array(rflist(self, 2)).T
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
