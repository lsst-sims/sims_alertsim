"""Instance Catalog"""
import numpy as np
from collections import OrderedDict
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catUtils.mixins import AstrometryStars, CameraCoords, PhotometryStars, Variability, VariabilityStars
from lsst.sims.catUtils.baseCatalogModels import *
from lsst.sims.catalogs.decorators import compound

def rf():
    """ Returns a random float """
    return np.random.ranf()

def rflist(catalog, count):
    """ List of random floats 

    @param [in] catalog is needed for the number of rows

    @param [in] count is the size of the list

    @param [out] rflist is a list (actually a 2d list)
    of random floats
    """

    rflist = []
    for i in range(0, count):
        rflist.append([rf()] * len(catalog.column_by_name('simobjid')))
    return rflist

def ri():
    """ Returns a random integer """
    return np.random.randint(1000)

def rbi():
    """ Returns a random big integer """
    return np.random.randint(0,9223372036854775807)
    
def array_to_dict(cols, vals):
    """ Turns a transposed list of tuples into a dictionary.
    Used for making nested data substructures

    @param [in] cols is a list with names of columns

    @param [in] vals is a transposed list of tuples

    @param [out] list_of_dicts is a list of dictionaries
    """

    list_of_dicts = []
    
    for val in vals:
        dicty = dict(zip(cols, val))
        list_of_dicts.append(dicty)
    return list_of_dicts

class VariableStars(InstanceCatalog,PhotometryStars,VariabilityStars):

    """ Class for describing variable stars output """

    catalog_type = 'variable_stars'

    column_outputs = ['id', 'raJ2000', 'decJ2000',
            'lsst_u', 'lsst_g', 'lsst_r',
            'lsst_i', 'lsst_z', 'lsst_y',
            'delta_lsst_u', 'delta_lsst_g',
            'delta_lsst_r', 'delta_lsst_i',
            'delta_lsst_z', 'delta_lsst_y',
            #'sigma_lsst_u','sigma_lsst_g','sigma_lsst_r',
            #'sigma_lsst_i','sigma_lsst_z', 'sigma_lsst_y',
            'gal_l', 'gal_b', 'varParamStr']


    datatypes = ['uint64', 'double', 'double',
            'double', 'double', 'double',
            'double', 'double', 'double',
            'double', 'double', 'double',
            'double', 'double', 'double',
            'double', 'double', 'double',
            'double', 'double', 'string']

    ucds = ['meta.id', 'pos.eq.ra', 'pos.eq.dec',
                'phot.mag', 'phot.mag',
                'phot.mag', 'phot.mag',
                'phot.mag', 'phot.mag',
                'phot.mag', 'phot.mag',
                'phot.mag', 'phot.mag',
                'phot.mag', 'phot.mag',
                #'stat.error', 'stat.error',
                #'stat.error', 'stat.error',
                #'stat.error', 'stat.error',
                '', '', 'src.var',]

    units = ['', 'rad', 'rad', '', '', '',
             '', '', '', '', '', '',
            #'', '', '', '', '', '',
             '', '', '', '', '', '']

    @staticmethod
    def get_column_outputs(bandname):
        return ['id', 'raJ2000', 'decJ2000','lsst_'+bandname,
                'delta_lsst_'+bandname, 'sigma_lsst_'+bandname, 'varParamStr']

class VariableStarsDia(VariableStars):

    catalog_type = 'variable_stars_dia'

    # DIASource columns as of DPDD from May 6th 2016

    #column_outputs = VariableStars.column_outputs + ['diaSourceId', 'ccdVisitId',
    
    """
    differences between DPDD and L1 schema
    N = Ndata
    fpFlux, fpFluxSigma = totFlux, totFluxErr
    diffFluxSigma = diffFluxErr
    fpSky, fpSkySigma = fpBkgd, fpBkgdErr
    """

    column_outputs = ['diaSourceId', 'ccdVisitId',
          'diaObjectId', 'ssObjectId', 'parentSourceId', 'midPointTai',
          'filterName', 'radec', 'radecCov', 'xy', 'xyCov', 'apFlux', 'apFluxErr', 'snr',
          'psFlux', 'psRadec', 'psCov', 'psLnL', 'psChi2', 'psN', 'trailFlux',
          'trailRadec', 'trailLength', 'trailAngle', 'trailCov', 'trailLnL',
          'trailChi2', 'trailN', 'dipMeanFlux', 'dipFluxDiff', 'dipRadec',
          'dipLength', 'dipAngle', 'dipCov', 'dipLnL', 'dipChi2', 'dipN',
          'totFlux', 'totFluxErr', 'diffFlux', 'diffFluxSigma', 'fpBkgd', 'fpBkgdErr',
          'Ixx', 'Iyy', 'Ixy', 'Icov', 'IxxPSF', 'IyyPSF', 'IxyPSF', 'extendedness',
          'spuriousness', 'flags',]

    # UCD's - Veljko's best guesses. Check this one day please

    #ucds = VariableStars.ucds + ['meta.id;meta.main', 'meta.id;instr.param',
    ucds = ['meta.id;meta.main', 'meta.id;instr.param',
                'meta.id.assoc', 'meta.id.assoc', 'meta.id.parent',
                'time.epoch', 'instr.filter', 'pos.eq.ra;pos.eq.dec;meta.main',
                'stat.covariance;pos.eq','instr.pixel', 'stat.covariance',
                'phot.flux;arith.diff;phot.calib',
                'stat.error;phot.flux', 'stat.snr',
                'phot.flux;arith.diff', 'pos.eq.ra;pos.eq.dec', 'stat.covariance;pos.eq',
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

    #units = VariableStars.units + ['', '', '', '', '', 'time', 'degrees',
    units = ['', '', '', '', '', 'time', '', 'degrees',
             'various', 'pixels', 'various', 'nmgy', 'nmgy', 'nmgy',
             'degrees', 'various', '', '', '', 'nmgy', 'degrees', 'arcsec',
             'degrees', 'various', '', '', '', 'nmgy', 'nmgy', 'degrees',
             'arcsec', 'degrees', 'various', '', '', '', 'nmgy', 'nmgy',
             'nmgy', 'nmgy', 'nmgy/asec^2', 'nmgy/asec^2', 'nmgy/asec^2',
             'nmgy/asec^2', 'nmgy/asec^2', 'nmgy^2 asec^4', 'nmgy/asec^2',
             'nmgy/asec^2', 'nmgy/asec^2', '', '', 'bit',]

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
          ('diffFlux', rf(), float), ('diffFluxSigma', rf(), float),
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
        return self.column_by_name('simobjid')

    def get_radec(self):
        ra = self.column_by_name('raJ2000')
        dec = self.column_by_name('decJ2000')
        vals = np.array([ra, dec]).T
        cols = ['ra', 'decl']
        return array_to_dict(cols, vals)

    # DIASource attributes in a form of a list
    # with randomly assigned values (for the time being)

    def get_radecCov(self):
        vals = np.array(rflist(self, 3)).T
        cols = ['raSigma', 'declSigma', 'ra_decl_Cov']
        return array_to_dict(cols, vals)


    def get_xy(self):
        vals = np.array(rflist(self, 2)).T
        cols = ['x', 'y']
        return array_to_dict(cols, vals)

    def get_xyCov(self):
        vals = np.array(rflist(self, 3)).T
        cols = ['xSigma', 'ySigma', 'x_y_Cov']
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
        cols = ['psCov01', 'psCov02', 'psCov03', 'psCov04', 
                'psCov05', 'psCov06']
        return array_to_dict(cols, vals)

    def get_trailRadec(self):
        vals = np.array(rflist(self, 2)).T
        cols = ['trailRa', 'trailDec']
        return array_to_dict(cols, vals)

    def get_trailCov(self):
        vals = np.array(rflist(self, 15)).T
        cols = ['trailCov01', 'trailCov02', 'trailCov03', 
                'trailCov04', 'trailCov05', 'trailCov06', 
                'trailCov07', 'trailCov08', 'trailCov09', 
                'trailCov10', 'trailCov11', 'trailCov12', 
                'trailCov13', 'trailCov14', 'trailCov15']
        return array_to_dict(cols, vals)

    def get_dipRadec(self):
        vals = np.array(rflist(self, 2)).T
        cols = ['dipRa', 'dipDec']
        return array_to_dict(cols, vals)

    def get_dipCov(self):
        vals = np.array(rflist(self, 15)).T
        cols = ['dipCov01', 'dipCov02', 'dipCov03', 
                'dipCov04', 'dipCov05', 'dipCov06', 
                'dipCov07', 'dipCov08', 'dipCov09', 
                'dipCov10', 'dipCov11', 'dipCov12', 
                'dipCov13', 'dipCov14', 'dipCov15']
        return array_to_dict(cols, vals)

    def get_Icov(self):
        vals = np.array(rflist(self, 6)).T
        cols = ["Icov01", "Icov02", "Icov03", 
                "Icov04", "Icov05", "Icov06"]
        return array_to_dict(cols, vals)

    # resolve db column case-sensitivness
    #def get_htmId20(self):
    #    return self._decapitalize_column_name('htmID')

    def _decapitalize_column_name(self, colname):
        if colname in  self.db_obj.columnMap.keys():
            return self.column_by_name(colname)
        else:
            return self.column_by_name(colname.lower())

class VariabilityDummy(Variability):
    """ Dummy class for avoiding InstanceCatalog inheritance """
    # include obs_metadata getter/setter in VariabilityMixin ?
    def __init__(self, obs_metadata):
        self.obs_metadata = obs_metadata


class VanillaStars(InstanceCatalog):

    catalog_type = 'vanilla_stars'

    column_outputs = ['ra', 'decl', 'rmag']
    ucds = ['pos.eq.ra', 'pos.eq.dec', 'phot.mag']
    units = ['rad', 'rad', '']

"""

class DIASources(InstanceCatalog):
    catalog_type = 'DIA_sources'
    column_outputs = ['diaSourceId', 'ccdVisitId', 'diaObjectId', 'ssObjectId',
          'parentDiaSourceId', 'filterName', 'procHistoryId',
          'ssObjectReassocTime', 'midPointTai', 'ra', 'raSigma', 'decl',
          'declSigma', 'ra_decl_Cov', 'x', 'xSigma', 'y', 'ySigma',
          'x_y_Cov', 'snr', 'psFlux', 'psFluxSigma', 'psLnL', 'psChi2',
          'psN', 'trailFlux', 'trailFluxSigma', 'trailLength',
          'trailLengthSigma', 'trailAngle', 'trailAngleSigma',
          'trailFlux_trailLength_Cov', 'trailFlux_trailAngle_Cov',
          'trailLength_trailAngle_Cov', 'trailLnL', 'trailChi2', 'trailN',
          'fpFlux', 'fpFluxSigma', 'diffFlux', 'diffFluxSigma', 'fpSky',
          'fpSkySigma', 'E1', 'E1Sigma', 'E2', 'E2Sigma', 'E1_E2_Cov', 'mSum',
          'mSumSigma', 'extendedness', 'apMeanSb01', 'apMeanSb01Sigma',
          'apMeanSb02', 'apMeanSb02Sigma', 'apMeanSb03', 'apMeanSb03Sigma',
          'apMeanSb04', 'apMeanSb04Sigma', 'apMeanSb05', 'apMeanSb05Sigma',
          'apMeanSb06', 'apMeanSb06Sigma', 'apMeanSb07', 'apMeanSb07Sigma',
          'apMeanSb08', 'apMeanSb08Sigma', 'apMeanSb09', 'apMeanSb09Sigma',
          'apMeanSb10', 'apMeanSb10Sigma', 'flags', 'htmId20', 'varParamStr']
    default_columns = [('diaSourceId', rbi(), int), ('ccdVisitId', rbi(), int),
          ('diaObjectId', rbi(), int), ('ssObjectId', rbi(), int),
          ('parentDiaSourceId', rbi(), int), ('filterName', 0, (str,1)),
          ('procHistoryId', rbi(), int), ('ssObjectReassocTime', ri(), str),
	      ('midPointTai', rf(), float), ('ra', rf(), float), ('raSigma', rf(), float),
          ('decl', rf(), float), ('declSigma', rf(), float),
          ('ra_decl_Cov', rf(), float), ('x', rf(), float), ('xSigma', rf(), float),
          ('y', rf(), float), ('ySigma', rf(), float), ('x_y_Cov', rf(), float),
          ('snr', rf(), float), ('psFlux', rf(), float), ('psFluxSigma', rf(), float),
          ('psLnL', rf(), float), ('psChi2', rf(), float), ('psN', ri(), int),
          ('trailFlux', rf(), float), ('trailFluxSigma', rf(), float),
          ('trailLength', rf(), float), ('trailLengthSigma', rf(), float),
          ('trailAngle', rf(), float), ('trailAngleSigma', rf(), float),
          ('trailFlux_trailLength_Cov', rf(), float),
          ('trailFlux_trailAngle_Cov', rf(), float),
          ('trailLength_trailAngle_Cov', rf(), float), ('trailLnL', rf(), float),
          ('trailChi2', rf(), float), ('trailN', ri(), int), ('fpFlux', rf(), float),
          ('fpFluxSigma', rf(), float), ('diffFlux', rf(), float),
          ('diffFluxSigma', rf(), float), ('fpSky', rf(), float),
          ('fpSkySigma', rf(), float), ('E1', rf(), float), ('E1Sigma', rf(), float),
          ('E2', rf(), float), ('E2Sigma', rf(), float), ('E1_E2_Cov', rf(), float),
          ('mSum', rf(), float), ('mSumSigma', rf(), float),
          ('extendedness', rf(), float),
          ('apMeanSb01', rf(), float), ('apMeanSb01Sigma', rf(), float),
          ('apMeanSb02', rf(), float), ('apMeanSb02Sigma', rf(), float),
          ('apMeanSb03', rf(), float), ('apMeanSb03Sigma', rf(), float),
          ('apMeanSb04', rf(), float), ('apMeanSb04Sigma', rf(), float),
          ('apMeanSb05', rf(), float), ('apMeanSb05Sigma', rf(), float),
          ('apMeanSb06', rf(), float), ('apMeanSb06Sigma', rf(), float),
          ('apMeanSb07', rf(), float), ('apMeanSb07Sigma', rf(), float),
          ('apMeanSb08', rf(), float), ('apMeanSb08Sigma', rf(), float),
          ('apMeanSb09', rf(), float), ('apMeanSb09Sigma', rf(), float),
          ('apMeanSb10', rf(), float), ('apMeanSb10Sigma', rf(), float),
          ('flags', rbi(), int), ('htmId20', rbi(), int),
          ('varParamString', 0, (str,1))]

    def get_diaSourceId(self):
        return self.column_by_name('simobjid')

    def get_htmId20(self):
	    return self.column_by_name('htmid')
	    #return self.column_by_name('htmID')

    @staticmethod
    def get_ucds():
        return ['meta.id;obs.image', 'meta.id;obs.image', 'meta.id;src',
                'meta.id;src', 'meta.id;src', 'meta.id;instr.filter', '', '',
                'time.epoch', 'pos.eq.ra', 'stat.error;pos.eq.ra',
                'pos.eq.dec', 'stat.error;pos.eq.dec', '', 'pos.cartesian.x',
                'stat.error;pos.cartesian.x', 'pos.cartesian.y',
                'stat.error;pos.cartesian.y', '', '', 'phot.count', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                'phot.count','stat.error;phot.count', '',
                'stat.error;phot.count', '', '', 'phys.size.axisRatio',
                'stat.error;phys.size.axisRatio', 'phys.size.axisRatio',
                'stat.error;phys.size.axisRatio', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', 'meta.code', 'src.var']

    @staticmethod
    def get_units():
        return ['','','','','','','','','d','deg','deg','deg','deg','deg^2','pixel',
            'pixel','pixel','pixel','pixel^2','','nmgy','nmgy','','','','nmgy',
            'nmgy','arcsec','nmgy','degrees','nmgy','','','','','','','nmgy',
            'nmgy','nmgy','nmgy','nmgy/asec^2','nmgy/asec^2','','','','','','',
            '','','','','','','','','','','','','','','','','','','','','','','','']

    @staticmethod
    def get_datatypes():
        return ['BIGINT','BIGINT','BIGINT','BIGINT','BIGINT','CHAR(1)','BIGINT',
            'DATETIME','DOUBLE','DOUBLE','FLOAT','DOUBLE','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','INT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','INT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','BIGINT','BIGINT','STRING']

    @staticmethod
    def get_descriptions():
        return ['Unique id.',
                'Id of the ccdVisit where this diaSource was measured. Note that we are allowing a diaSource to belong to multiple amplifiers, but it may not span multiple ccds.',
            'Id of the diaObject this source was associated with, if any. If not, it is set to NULL (each diaSource will be associated with either a diaObject or ssObject).',
            'Id of the ssObject this source was associated with, if any. If not, it is set to NULL (each diaSource will be associated with either a diaObject or ssObject).',
            'Id of the parent diaSource this diaObject has been deblended from, if any.',
            'Name of the filter used to take the Visit where this diaSource was measured.',
            'Pointer to ProcessingHistory table.',
            'Time when this diaSource was reassociated from diaObject to ssObject (if such reassociation happens, otherwise NULL).',
            'Effective mid-exposure time for this diaSource.',
            'RA-coordinate of the center of this diaSource.','Uncertainty of ra.',
            'Decl-coordinate of the center of this diaSource.','Uncertainty of decl.',
            'Covariance between ra and decl.',
            'x position computed by a centroiding algorithm.','Uncertainty of x.',
            'y position computed by a centroiding algorithm.','Uncertainty of y.',
            'Covariance between x and y.',
            'The signal-to-noise ratio at which this source was detected in the difference image.',
            'Calibrated flux for Point Source model. Note this actually measures the flux difference between the template and the visit image.',
            'Uncertainty of psFlux.',
            'Natural log likelihood of the observed data given the Point Source model.',
            'Chi^2 static of the model fit.',
            'The number of data points (pixels) used to fit the model.',
            'Calibrated flux for a trailed source model. Note this actually measures the flux difference between the template and the visit image.',
            'Uncertainty of trailFlux.',
            'Maximum likelihood fit of trail length.','Uncertainty of trailLength.',
            'Maximum likelihood fit of the angle between the meridian through the centroid and the trail direction (bearing).',
            'Uncertainty of trailAngle.','Covariance of trailFlux and trailLength',
            'Covariance of trailFlux and trailAngle','Covariance of trailLength and trailAngle',
            'Natural log likelihood of the observed data given the trailed Point Source model.',
            'Chi^2 static of the model fit.','The number of data points (pixels) used to fix the model.',
            'Calibrated flux for Point Source model measured on the visit image centered at the centroid measured on the difference image (forced photometry flux).',
            'Uncertainty of fpFlux',
            'Calibrated flux for Point Source model centered on radec but measured on the difference of snaps comprising this visit.',
            'Uncertainty of diffFlux',
            'Estimated sky background at the position (centroid) of the object.',
            'Uncertainty of fpSky.',
            'Adaptive e1 shape measure of the source as measured on the difference image.',
            'Uncertainty of E1.',
            'Adaptive e2 shape measure of the source as measured on the difference image.',
            'Uncertainty of E2.','Covariance of E1 and E2',
            'Sum of second adaptive moments.','Uncertainty of mSum.','A measure of extendedness, Computed using a combination of available moments and model fluxes or from a likelihood ratio of point/trailed source models (exact algorithm TBD). extendedness = 1 implies a high degree of confidence that the source is extended. extendedness = 0 implies a high degree of confidence that the source is point-like.','Mean surface brightness at which the aperture measurement is being performed.','Standard deviation of pixel surface brightness in annulus.','Mean surface brightness at which the aperture measurement is being performed.','Standard deviation of pixel surface brightness in annulus.','Mean surface brightness at which the aperture measurement is being performed.','Standard deviation of pixel surface brightness in annulus.','Mean surface brightness at which the aperture measurement is being performed.','Standard deviation of pixel surface brightness in annulus.','Mean surface brightness at which the aperture measurement is being performed.','Standard deviation of pixel surface brightness in annulus.',
            'Mean surface brightness at which the aperture measurement is being performed.',
            'Standard deviation of pixel surface brightness in annulus.',
            'Mean surface brightness at which the aperture measurement is being performed.',
            'Standard deviation of pixel surface brightness in annulus.',
            'Mean surface brightness at which the aperture measurement is being performed.',
            'Standard deviation of pixel surface brightness in annulus.',
            'Mean surface brightness at which the aperture measurement is being performed.',
            'Standard deviation of pixel surface brightness in annulus.',
            'Mean surface brightness at which the aperture measurement is being performed.',
            'Standard deviation of pixel surface brightness in annulus.',
            'Flags, bitwise OR tbd.','HTM index.']

class DIAObjects(InstanceCatalog):
    catalog_type = 'DIA_objects'
    column_outputs = ['diaObjectId','procHistoryId','validityStart','validityEnd',
		      'ra','raSigma','decl','declSigma','ra_decl_Cov','muRa','muRaSigma',
		      'muDecl','muDecSigma','muRa_muDeclCov','parallax','parallaxSigma',
		      'muRa_parallax_Cov','muDecl_parallax_Cov','lnL','chi2','N',
		      'uPSFlux','uPSFluxErr','uPSFluxSigma','uFPFlux','uFPFluxErr',
		      'uFPFluxSigma','gPSFlux','gPSFluxErr','gPSFluxSigma','gFPFlux',
		      'gFPFluxErr','gFPFluxSigma','rPSFlux','rPSFluxErr','rPSFluxSigma',
		      'rFPFlux','rFPFluxErr','rFPFluxSigma','iPSFlux','iPSFluxErr',
		      'iPSFluxSigma','iFPFlux','iFPFluxErr','iFPFluxSigma','zPSFlux',
		      'zPSFluxErr','zPSFluxSigma','zFPFlux','zFPFluxErr','zFPFluxSigma',
		      'yPSFlux','yPSFluxErr','yPSFluxSigma','yFPFlux','yFPFluxErr',
		      'yFPFluxSigma','uLcPeriodic','gLcPeriodic','rLcPeriodic',
		      'iLcPeriodic','zLcPeriodic','yLcPeriodic','uLcNonPeriodic',
		      'gLcNonPeriodic','rLcNonPeriodic','iLcNonPeriodic','zLcNonPeriodic',
		      'yLcNonPeriodic','nearbyObj1','nearbyObj1Dist','nearbyObj1LnP',
		      'nearbyObj2','nearbyObj2Dist','nearbyObj2LnP','nearbyObj3',
		      'nearbyObj3Dist','nearbyObj3LnP','flags','htmId20']
    default_columns = [('diaObjectId', rbi(), int), ('procHistoryId', rbi(), int),
                       ('validityStart', 0, str), ('validityEnd', 0, str),
                       ('ra', rf(), float), ('raSigma', rf(), float), ('decl', rf(), float),
                       ('declSigma', rf(), float), ('ra_decl_Cov', rf(), float),
                       ('muRa', rf(), float), ('muRaSigma', rf(), float),
                       ('muDecl', rf(), float), ('muDecSigma', rf(), float),
                       ('muRa_muDeclCov', rf(), float), ('parallax', rf(), float),
                       ('parallaxSigma', rf(), float), ('muRa_parallax_Cov', rf(), float),
                       ('muDecl_parallax_Cov', rf(), float), ('lnL', rf(), float),
                       ('chi2', rf(), float), ('N', ri(), int), ('uPSFlux', rf(), float),
                       ('uPSFluxErr', rf(), float), ('uPSFluxSigma', rf(), float),
                       ('uFPFlux', rf(), float), ('uFPFluxErr', rf(), float),
                       ('uFPFluxSigma', rf(), float), ('gPSFlux', rf(), float),
                       ('gPSFluxErr', rf(), float), ('gPSFluxSigma', rf(), float),
                       ('gFPFlux', rf(), float), ('gFPFluxErr', rf(), float),
                       ('gFPFluxSigma', rf(), float), ('rPSFlux', rf(), float),
                       ('rPSFluxErr', rf(), float), ('rPSFluxSigma', rf(), float),
                       ('rFPFlux', rf(), float), ('rFPFluxErr', rf(), float),
                       ('rFPFluxSigma', rf(), float), ('iPSFlux', rf(), float),
                       ('iPSFluxErr', rf(), float), ('iPSFluxSigma', rf(), float),
                       ('iFPFlux', rf(), float), ('iFPFluxErr', rf(), float),
                       ('iFPFluxSigma', rf(), float), ('zPSFlux', rf(), float),
                       ('zPSFluxErr', rf(), float), ('zPSFluxSigma', rf(), float),
                       ('zFPFlux', rf(), float), ('zFPFluxErr', rf(), float),
                       ('zFPFluxSigma', rf(), float), ('yPSFlux', rf(), float),
                       ('yPSFluxErr', rf(), float), ('yPSFluxSigma', rf(), float),
                       ('yFPFlux', rf(), float), ('yFPFluxErr', rf(), float),
                       ('yFPFluxSigma', rf(), float), ('uLcPeriodic', rf(), float),
                       ('gLcPeriodic', rf(), float), ('rLcPeriodic', rf(), float),
                       ('iLcPeriodic', rf(), float), ('zLcPeriodic', rf(), float),
                       ('yLcPeriodic', rf(), float), ('uLcNonPeriodic', rf(), float),
                       ('gLcNonPeriodic', rf(), float), ('rLcNonPeriodic', rf(), float),
                       ('iLcNonPeriodic', rf(), float), ('zLcNonPeriodic', rf(), float),
                       ('yLcNonPeriodic', rf(), float), ('nearbyObj1', rbi(), int),
                       ('nearbyObj1Dist', rf(), float), ('nearbyObj1LnP', rf(), float),
                       ('nearbyObj2', rbi(), int), ('nearbyObj2Dist', rf(), float),
                       ('nearbyObj2LnP', rf(), float), ('nearbyObj3', rbi(), int),
                       ('nearbyObj3Dist', rf(), float), ('nearbyObj3LnP', rf(), float),
                       ('flags', rbi(), int), ('htmId20', rbi(), int)]

    def get_diaObjectId(self):
        return self.column_by_name('simobjid')

    def get_muRa(self):
        return self.column_by_name('mura')

    def get_muDecl(self):
        return self.column_by_name('mudecl')

    @staticmethod
    def get_ucds():
        return ['meta.id;src','','','','pos.eq.ra','stat.error;pos.eq.ra','pos.eq.dec',
                'stat.error;pos.eq.dec','','pos.pm','stat.error;pos.pm','pos.pm',
                'stat.error;pos.pm','stat.covariance;pos.eq','pos.parallax',
                'stat.error;pos.parallax','','','','','','phot.count','','','phot.count',
                '','','phot.count','','','phot.count','','','phot.count','','',
                'phot.count','','','phot.count','','','phot.count','','','phot.count',
                '','','phot.count','','','phot.count','phot.count','phot.count',
                'phot.count','phot.count','phot.count','','','','','','','','','',
                '','','','meta.id;src','','','meta.id;src','','','meta.id;src','','',
                'meta.code']

    @staticmethod
    def get_units():
        return ['','','','','deg','deg','deg','deg','deg^2','mas/yr','mas/yr',
                'mas/yr','mas/yr','(mas/yr)^2','mas','mas','','','','','',
                'nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy',
                'nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy',
                'nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy',
                'nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy',
                '','','','','','','','','','','','','','arcsec','','','arcsec',
                '','','arcsec','','']

    @staticmethod
    def get_datatypes():
        return ['BIGINT','BIGINT','DATETIME','DATETIME','DOUBLE','FLOAT','DOUBLE',
                'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
                'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','INT','FLOAT','FLOAT',
                'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
                'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
                'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
                'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
                'FLOAT','FLOAT','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB',
                'BLOB','BLOB','BLOB','BLOB','BLOB','BIGINT','FLOAT','FLOAT',
                'BIGINT','FLOAT','FLOAT','BIGINT','FLOAT','FLOAT','BIGINT','BIGINT']

    @staticmethod
    def get_descriptions():
        return ['Unique id.',
                'Pointer to ProcessingHistory table.',
                'Time when validity of this diaObject starts.',
                'Time when validity of this diaObject ends.',
                'RA-coordinate of the center of this diaObject.',
                'Uncertainty of ra.',
                'Decl-coordinate of the center of this diaObject.',
                'Uncertainty of decl.',
                'Covariance between ra and decl.',
                'Proper motion (ra).',
                'Uncertainty of muRa.',
                'Proper motion (decl).',
                'Uncertainty of muDecl.',
                'Covariance of muRa and muDecl.',
                'Parallax.',
                'Uncertainty of parallax.',
                'Covariance of muRa and parallax.',
                'Covariance of muDecl and parallax.',
                'Natural log of the likelihood of the linear proper motion parallax fit.',
                'Chi^2 static of the model fit.',
                'The number of data points (pixels) used to fit the model.',
                'Weighted mean point-source model magnitude for u filter.',
                'Standard error of uPSFlux.','Uncertainty of uPSFlux.',
                'Weighted mean forced photometry flux for u fliter.',
                'Standard error of uFPFlux.','Uncertainty of uFPFlux.',
                'Weighted mean point-source model magnitude for g filter.',
                'Standard error of gPSFlux.','Uncertainty of gPSFlux.',
                'Weighted mean forced photometry flux for g fliter.',
                'Standard error of gFPFlux.','Uncertainty of gFPFlux.',
                'Weighted mean point-source model magnitude for u filter.',
                'Standard error of rPSFlux.','Uncertainty of rPSFlux.',
                'Weighted mean forced photometry flux for r fliter.',
                'Standard error of rFPFlux.','Uncertainty of rFPFlux.',
                'Weighted mean point-source model magnitude for i filter.',
                'Standard error of iPSFlux.','Uncertainty of iPSFlux.',
                'Weighted mean forced photometry flux for i fliter.',
                'Standard error of iFPFlux.','Uncertainty of uFPFlux.',
                'Weighted mean point-source model magnitude for z filter.',
                'Standard error of zPSFlux.','Uncertainty of zPSFlux.',
                'Weighted mean forced photometry flux for z fliter.',
                'Standard error of zFPFlux.','Uncertainty of zFPFlux.',
                'Weighted mean point-source model magnitude for y filter.',
                'Standard error of yPSFlux.','Uncertainty of yPSFlux.',
                'Weighted mean forced photometry flux for y fliter.',
                'Standard error of yFPFlux.','Uncertainty of yFPFlux.',
                'Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for u filter. [32 FLOAT].',
                'Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for g filter. [32 FLOAT].',
                'Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for r filter. [32 FLOAT].',
                'Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for i filter. [32 FLOAT].',
                'Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for z filter. [32 FLOAT].',
                'Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for y filter. [32 FLOAT].',
                'Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for u filter. [20 FLOAT].',
                'Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for g filter. [20 FLOAT].',
                'Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for r filter. [20 FLOAT].',
                'Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for i filter. [20 FLOAT].',
                'Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for z filter. [20 FLOAT].',
                'Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for y filter. [20 FLOAT].',
                'Id of the closest nearby object.','Distance to nearbyObj1.',
                'Natural log of the probability that the observed diaObject is the same as the nearbyObj1.',
                'Id of the second-closest nearby object.','Distance to nearbyObj2.',
                'Natural log of the probability that the observed diaObject is the same as the nearbyObj2.',
                'Id of the third-closest nearby object.','Distance to nearbyObj3.',
                'Natural log of the probability that the observed diaObject is the same as the nearbyObj3.',
                'Flags, bitwise OR tbd.','HTM index.']
    """
