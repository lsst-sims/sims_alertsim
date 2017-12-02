import numpy as np
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catUtils.mixins import AstrometryStars, PhotometryStars, Variability, VariabilityStars
from lsst.sims.alertsim.catalogs import DiaSourceCommons

__all__ = ["BasicVarStars", "DiaSourceVarStars", "VariabilityDummy",
           "VanillaStars"]


class BasicVarStars(InstanceCatalog, 
        PhotometryStars, VariabilityStars, AstrometryStars):

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
             '', '', '', '', '', '',
             '', '', '']

    @staticmethod
    def get_column_outputs(bandname):
        return ['id', 'raJ2000', 'decJ2000','lsst_'+bandname,
                'delta_lsst_'+bandname, 'sigma_lsst_'+bandname, 'varParamStr']

class DiaSourceVarStars(DiaSourceCommons, BasicVarStars):

    catalog_type = 'variable_stars_dia'
    column_outputs = DiaSourceCommons.column_outputs + BasicVarStars.column_outputs
    ucds = DiaSourceCommons.ucds + BasicVarStars.ucds
    datatypes = DiaSourceCommons.datatypes + BasicVarStars.datatypes
    units = DiaSourceCommons.units + BasicVarStars.units

    def get_ssObjectId(self):
        """
        Stars should not have an ssObjectId; their unique identifier is
        diaObjectId
        """
        return np.array([None]*len(self.column_by_name('uniqueId')))

    def get_diaObjectId(self):
        return self.column_by_name('uniqueId')


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
