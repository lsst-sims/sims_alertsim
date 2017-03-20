"""NOT YET WRITTEN"""
import numpy as np
from collections import OrderedDict
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catalogs.decorators import compound

"""
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
