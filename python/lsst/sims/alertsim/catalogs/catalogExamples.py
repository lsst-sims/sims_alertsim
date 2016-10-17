"""Instance Catalog"""
import numpy
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catUtils.mixins import AstrometryStars, CameraCoords, PhotometryStars, Variability, VariabilityStars
from lsst.sims.catUtils.baseCatalogModels import *

def rf():
    """ random float """
    return numpy.random.ranf()

def ri():
    """ random integer """
    return numpy.random.randint(1000)

def rbi():
    """ random big integer """
    return numpy.random.randint(0,9223372036854775807)

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
    
    column_outputs = VariableStars.column_outputs + ['diaSourceId', 'ccdVisitId', 'diaObjectId', 'ssObjectId',
          'parentDiaSourceId', 'filterName', 'procHistoryId',
          'ssObjectReassocTime', 'midPointTai', 'raSigma',
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
          'apMeanSb10', 'apMeanSb10Sigma', 'flags', 'htmId20',]

    ucds = VariableStars.ucds + ['meta.id;obs.image', 'meta.id;obs.image', 'meta.id;src', 
                'meta.id;src', 'meta.id;src', 'meta.id;instr.filter', '', '', 
                'time.epoch', 'stat.error;pos.eq.ra', 
                'stat.error;pos.eq.dec', '', 'pos.cartesian.x', 
                'stat.error;pos.cartesian.x', 'pos.cartesian.y', 
                'stat.error;pos.cartesian.y', '', '', 'phot.count', '', '', 
                '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                'phot.count','stat.error;phot.count', '', 
                'stat.error;phot.count', '', '', 'phys.size.axisRatio', 
                'stat.error;phys.size.axisRatio', 'phys.size.axisRatio', 
                'stat.error;phys.size.axisRatio', '', '', '', '', '', '', '', 
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 
                '', '', 'meta.code',]

    units = VariableStars.units + ['','','','','','','','','d','deg','deg','deg^2','pixel',
             'pixel','pixel','pixel','pixel^2','','nmgy','nmgy','','','','nmgy',
             'nmgy','arcsec','nmgy','degrees','nmgy','','','','','','','nmgy',
             'nmgy','nmgy','nmgy','nmgy/asec^2','nmgy/asec^2','','','','','','',
             '','','','','','','','','','','','','','','','','','','','','','','']
    
    default_columns = [('diaSourceId', rbi(), int), ('ccdVisitId', rbi(), int), 
          ('diaObjectId', rbi(), int), ('ssObjectId', rbi(), int), 
          ('parentDiaSourceId', rbi(), int), ('filterName', 0, (str,1)), 
          ('procHistoryId', rbi(), int), ('ssObjectReassocTime', ri(), str), 
	      ('midPointTai', rf(), float), ('raSigma', rf(), float), ('declSigma', rf(), float), 
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
          ('flags', rbi(), int), ('htmId20', rbi(), int),]

    def get_diaSourceId(self):
        return self.column_by_name('simobjid')

    # resolve db column case-sensitivness
    def get_htmId20(self):
        return self._decapitalize_column_name('htmID')

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