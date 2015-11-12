"""Instance Catalog"""
import numpy
from lsst.sims.catalogs.measures.instance import InstanceCatalog
from lsst.sims.coordUtils.Astrometry import AstrometryStars, CameraCoords
from lsst.sims.photUtils.Photometry import PhotometryStars
from lsst.obs.lsstSim.utils import loadCamera
from lsst.sims.photUtils.Variability import Variability, VariabilityStars
# from sqlalchemy import BIGINT, BINARY, BLOB, BOOLEAN, CHAR, DATE, DATETIME, INTEGER, FLOAT, NCHAR, NUMERIC, NVARCHAR, SMALLINT, TEXT, TIME, TIMESTAMP, VARBINARY

class VariableStars(InstanceCatalog,PhotometryStars,VariabilityStars):

    """
    def __init__(self, band):
        column_outputs += [band, band + '_var']
    """
    
    catalog_type = 'variable_stars'
    """
    column_outputs = ['id','raJ2000','decJ2000',
                      'lsst_u','lsst_g','lsst_r','lsst_i','lsst_z','lsst_y',
                      'delta_lsst_u','delta_lsst_g','delta_lsst_r','delta_lsst_i','delta_lsst_z',
                      'delta_lsst_y']
    """
    column_outputs = ['id','raJ2000','decJ2000',
                      'lsst_u','lsst_g','lsst_r','lsst_i','lsst_z','lsst_y',
                      'lsst_u_var','lsst_g_var','lsst_r_var','lsst_i_var','lsst_z_var',
                      'lsst_y_var']
    def get_ucds(self):
        return ['meta.id', 'pos.eq.ra', 'pos.eq.dec', 
                'phot.mag', 'phot.mag','phot.mag','phot.mag','phot.mag','phot.mag',
                'phot.mag', 'phot.mag','phot.mag','phot.mag','phot.mag','phot.mag' ]

    def get_units(self):
        return ['', 'rad', 'rad', 
                '', '', '', '', '', '',
                '', '', '', '', '', '' ]

class VanillaStars(InstanceCatalog):
    catalog_type = 'vanilla_stars'
    column_outputs = ['ra', 'decl', 'rmag']

    def get_ucds(self):
        return ['pos.eq.ra', 'pos.eq.dec', 'phot.mag']

    def get_units(self):
        return ['rad', 'rad', '']

class DIASources(InstanceCatalog):
    catalog_type = 'DIA_sources'
    column_outputs = ['diaSourceId','ccdVisitId','diaObjectId','ssObjectId',
          'parentDiaSourceId','filterName','procHistoryId','ssObjectReassocTime',
          'midPointTai','ra','raSigma','decl','declSigma','ra_decl_Cov','x',
          'xSigma','y','ySigma','x_y_Cov','snr','psFlux','psFluxSigma','psLnL',
          'psChi2','psN','trailFlux','trailFluxSigma','trailLength',
          'trailLengthSigma','trailAngle','trailAngleSigma',
          'trailFlux_trailLength_Cov','trailFlux_trailAngle_Cov',
          'trailLength_trailAngle_Cov','trailLnL','trailChi2','trailN',
          'fpFlux','fpFluxSigma','diffFlux','diffFluxSigma','fpSky','fpSkySigma',
          'E1','E1Sigma','E2','E2Sigma','E1_E2_Cov','mSum','mSumSigma',
          'extendedness','apMeanSb01','apMeanSb01Sigma','apMeanSb02',
          'apMeanSb02Sigma','apMeanSb03','apMeanSb03Sigma','apMeanSb04',
          'apMeanSb04Sigma','apMeanSb05','apMeanSb05Sigma','apMeanSb06',
          'apMeanSb06Sigma','apMeanSb07','apMeanSb07Sigma','apMeanSb08',
          'apMeanSb08Sigma','apMeanSb09','apMeanSb09Sigma','apMeanSb10',
          'apMeanSb10Sigma','flags','htmId20']
    default_columns = [('diaSourceId', 0, int), ('ccdVisitId', 0, int), 
          ('diaObjectId', 0, int), ('ssObjectId', 0, int), 
          ('parentDiaSourceId', 0, int), ('filterName', 0, (str,1)), 
          ('procHistoryId', 0, int), ('ssObjectReassocTime', 0, str), 
          ('midPointTai', 0, float), ('ra', 0, float), ('raSigma', 0, float), 
          ('decl', 0, float), ('declSigma', 0, float), ('ra_decl_Cov', 0, float), 
          ('x', 0, float), ('xSigma', 0, float), ('y', 0, float), 
          ('ySigma', 0, float), ('x_y_Cov', 0, float), ('snr', 0, float), 
          ('psFlux', 0, float), ('psFluxSigma', 0, float), ('psLnL', 0, float), 
          ('psChi2', 0, float), ('psN', 0, int), ('trailFlux', 0, float), 
          ('trailFluxSigma', 0, float), ('trailLength', 0, float), 
          ('trailLengthSigma', 0, float), ('trailAngle', 0, float), 
          ('trailAngleSigma', 0, float), ('trailFlux_trailLength_Cov', 0, float), 
          ('trailFlux_trailAngle_Cov', 0, float), 
          ('trailLength_trailAngle_Cov', 0, float), ('trailLnL', 0, float), 
          ('trailChi2', 0, float), ('trailN', 0, int), ('fpFlux', 0, float), 
          ('fpFluxSigma', 0, float), ('diffFlux', 0, float), 
          ('diffFluxSigma', 0, float), ('fpSky', 0, float), ('fpSkySigma', 0, float), 
          ('E1', 0, float), ('E1Sigma', 0, float), ('E2', 0, float), 
          ('E2Sigma', 0, float), ('E1_E2_Cov', 0, float), ('mSum', 0, float), 
          ('mSumSigma', 0, float), ('extendedness', 0, float), 
          ('apMeanSb01', 0, float), ('apMeanSb01Sigma', 0, float), 
          ('apMeanSb02', 0, float), ('apMeanSb02Sigma', 0, float), 
          ('apMeanSb03', 0, float), ('apMeanSb03Sigma', 0, float), 
          ('apMeanSb04', 0, float), ('apMeanSb04Sigma', 0, float), 
          ('apMeanSb05', 0, float), ('apMeanSb05Sigma', 0, float), 
          ('apMeanSb06', 0, float), ('apMeanSb06Sigma', 0, float), 
          ('apMeanSb07', 0, float), ('apMeanSb07Sigma', 0, float), 
          ('apMeanSb08', 0, float), ('apMeanSb08Sigma', 0, float), 
          ('apMeanSb09', 0, float), ('apMeanSb09Sigma', 0, float), 
          ('apMeanSb10', 0, float), ('apMeanSb10Sigma', 0, float), 
          ('flags', 0, int), ('htmId20', 0, int)]

    def get_diaSourceId(self):
        return self.column_by_name('simobjid')
  
    def get_ucds(self):
        return ['meta.id;obs.image','meta.id;obs.image','meta.id;src','meta.id;src',
            'meta.id;src','meta.id;instr.filter','','','time.epoch','pos.eq.ra',
            'stat.error;pos.eq.ra','pos.eq.dec','stat.error;pos.eq.dec','',
            'pos.cartesian.x','stat.error;pos.cartesian.x','pos.cartesian.y',
            'stat.error;pos.cartesian.y','','','phot.count','','','','','','',
            '','','','','','','','','','','phot.count','stat.error;phot.count',
            '','stat.error;phot.count','','','phys.size.axisRatio',
            'stat.error;phys.size.axisRatio','phys.size.axisRatio',
            'stat.error;phys.size.axisRatio','','','','','','','','','','','',
            '','','','','','','','','','','','','','meta.code']
  
    def get_units(self):
        return ['','','','','','','','','d','deg','deg','deg','deg','deg^2','pixel',
            'pixel','pixel','pixel','pixel^2','','nmgy','nmgy','','','','nmgy',
            'nmgy','arcsec','nmgy','degrees','nmgy','','','','','','','nmgy',
            'nmgy','nmgy','nmgy','nmgy/asec^2','nmgy/asec^2','','','','','','',
            '','','','','','','','','','','','','','','','','','','','','','','']
  
    def get_datatypes(self):
        return ['BIGINT','BIGINT','BIGINT','BIGINT','BIGINT','CHAR(1)','BIGINT',
            'DATETIME','DOUBLE','DOUBLE','FLOAT','DOUBLE','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','INT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','INT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT',
            'FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','BIGINT','BIGINT']
  
    def get_descriptions(self):
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
  column_outputs = ['diaObjectId','procHistoryId','validityStart','validityEnd','ra','raSigma','decl','declSigma','ra_decl_Cov','muRa','muRaSigma','muDecl','muDecSigma','muRa_muDeclCov','parallax','parallaxSigma','muRa_parallax_Cov','muDecl_parallax_Cov','lnL','chi2','N','uPSFlux','uPSFluxErr','uPSFluxSigma','uFPFlux','uFPFluxErr','uFPFluxSigma','gPSFlux','gPSFluxErr','gPSFluxSigma','gFPFlux','gFPFluxErr','gFPFluxSigma','rPSFlux','rPSFluxErr','rPSFluxSigma','rFPFlux','rFPFluxErr','rFPFluxSigma','iPSFlux','iPSFluxErr','iPSFluxSigma','iFPFlux','iFPFluxErr','iFPFluxSigma','zPSFlux','zPSFluxErr','zPSFluxSigma','zFPFlux','zFPFluxErr','zFPFluxSigma','yPSFlux','yPSFluxErr','yPSFluxSigma','yFPFlux','yFPFluxErr','yFPFluxSigma','uLcPeriodic','gLcPeriodic','rLcPeriodic','iLcPeriodic','zLcPeriodic','yLcPeriodic','uLcNonPeriodic','gLcNonPeriodic','rLcNonPeriodic','iLcNonPeriodic','zLcNonPeriodic','yLcNonPeriodic','nearbyObj1','nearbyObj1Dist','nearbyObj1LnP','nearbyObj2','nearbyObj2Dist','nearbyObj2LnP','nearbyObj3','nearbyObj3Dist','nearbyObj3LnP','flags','htmId20']
  
  def get_ucds(self):
    return ['meta.id;src','','','','pos.eq.ra','stat.error;pos.eq.ra','pos.eq.dec','stat.error;pos.eq.dec','','pos.pm','stat.error;pos.pm','pos.pm','stat.error;pos.pm','stat.covariance;pos.eq','pos.parallax','stat.error;pos.parallax','','','','','','phot.count','','','phot.count','','','phot.count','','','phot.count','','','phot.count','','','phot.count','','','phot.count','','','phot.count','','','phot.count','','','phot.count','','','phot.count','phot.count','phot.count','phot.count','phot.count','phot.count','','','','','','','','','','','','','meta.id;src','','','meta.id;src','','','meta.id;src','','','meta.code']
  
  def get_units(self):
    return ['','','','','deg','deg','deg','deg','deg^2','mas/yr','mas/yr','mas/yr','mas/yr','(mas/yr)^2','mas','mas','','','','','','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','nmgy','','','','','','','','','','','','','','arcsec','','','arcsec','','','arcsec','','']
  
  def get_datatypes(self):
    return ['BIGINT','BIGINT','DATETIME','DATETIME','DOUBLE','FLOAT','DOUBLE','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','INT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BLOB','BIGINT','FLOAT','FLOAT','BIGINT','FLOAT','FLOAT','BIGINT','FLOAT','FLOAT','BIGINT','BIGINT']
  
  def get_descriptions(self):
    return ['Unique id.','Pointer to ProcessingHistory table.','Time when validity of this diaObject starts.','Time when validity of this diaObject ends.','RA-coordinate of the center of this diaObject.','Uncertainty of ra.','Decl-coordinate of the center of this diaObject.','Uncertainty of decl.','Covariance between ra and decl.','Proper motion (ra).','Uncertainty of muRa.','Proper motion (decl).','Uncertainty of muDecl.','Covariance of muRa and muDecl.','Parallax.','Uncertainty of parallax.','Covariance of muRa and parallax.','Covariance of muDecl and parallax.','Natural log of the likelihood of the linear proper motion parallax fit.','Chi^2 static of the model fit.','The number of data points (pixels) used to fit the model.','Weighted mean point-source model magnitude for u filter.','Standard error of uPSFlux.','Uncertainty of uPSFlux.','Weighted mean forced photometry flux for u fliter.','Standard error of uFPFlux.','Uncertainty of uFPFlux.','Weighted mean point-source model magnitude for g filter.','Standard error of gPSFlux.','Uncertainty of gPSFlux.','Weighted mean forced photometry flux for g fliter.','Standard error of gFPFlux.','Uncertainty of gFPFlux.','Weighted mean point-source model magnitude for u filter.','Standard error of rPSFlux.','Uncertainty of rPSFlux.','Weighted mean forced photometry flux for r fliter.','Standard error of rFPFlux.','Uncertainty of rFPFlux.','Weighted mean point-source model magnitude for i filter.','Standard error of iPSFlux.','Uncertainty of iPSFlux.','Weighted mean forced photometry flux for i fliter.','Standard error of iFPFlux.','Uncertainty of uFPFlux.','Weighted mean point-source model magnitude for z filter.','Standard error of zPSFlux.','Uncertainty of zPSFlux.','Weighted mean forced photometry flux for z fliter.','Standard error of zFPFlux.','Uncertainty of zFPFlux.','Weighted mean point-source model magnitude for y filter.','Standard error of yPSFlux.','Uncertainty of yPSFlux.','Weighted mean forced photometry flux for y fliter.','Standard error of yFPFlux.','Uncertainty of yFPFlux.','Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for u filter. [32 FLOAT].','Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for g filter. [32 FLOAT].','Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for r filter. [32 FLOAT].','Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for i filter. [32 FLOAT].','Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for z filter. [32 FLOAT].','Periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for y filter. [32 FLOAT].','Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for u filter. [20 FLOAT].','Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for g filter. [20 FLOAT].','Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for r filter. [20 FLOAT].','Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for i filter. [20 FLOAT].','Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for z filter. [20 FLOAT].','Non-periodic features extracted from light-curves using generalized Lomb-Scargle periodogram for y filter. [20 FLOAT].','Id of the closest nearby object.','Distance to nearbyObj1.','Natural log of the probability that the observed diaObject is the same as the nearbyObj1.','Id of the second-closest nearby object.','Distance to nearbyObj2.','Natural log of the probability that the observed diaObject is the same as the nearbyObj2.','Id of the third-closest nearby object.','Distance to nearbyObj3.','Natural log of the probability that the observed diaObject is the same as the nearbyObj3.','Flags, bitwise OR tbd.','HTM index.']
