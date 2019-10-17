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

    # attributes divided so that other catalogs can use
    # only parts they need
    basic_attributes = ['id', 'raJ2000', 'decJ2000',
            'gal_l', 'gal_b', 'varParamStr']
    total_mags = ['lsst_u', 'lsst_g', 'lsst_r',
            'lsst_i', 'lsst_z', 'lsst_y']
    delta_mags = ['delta_lsst_u', 'delta_lsst_g',
            'delta_lsst_r', 'delta_lsst_i',
            'delta_lsst_z', 'delta_lsst_y']
    sigma_mags = ['sigma_lsst_u', 'sigma_lsst_g',
            'sigma_lsst_r', 'sigma_lsst_i',
            'sigma_lsst_z', 'sigma_lsst_y']
    column_outputs = basic_attributes + total_mags + delta_mags

    # datatypes, ucds, units divided

    basic_datatypes = ['uint64', 'double', 'double',
            'double', 'double', 'string']
    mags_datatypes = ['double', 'double', 'double',
            'double', 'double', 'double']
    datatypes = basic_datatypes + mags_datatypes*2

    basic_ucds = ['meta.id', 'pos.eq.ra', 'pos.eq.dec',
                '', '', 'src.var']
    mags_ucds = ['phot.mag', 'phot.mag', 'phot.mag',
            'phot.mag', 'phot.mag', 'phot.mag']
    errors_ucds = ['stat.error', 'stat.error', 'stat.error', 
            'stat.error', 'stat.error', 'stat.error',]
    ucds = basic_ucds + mags_ucds*2

    basic_units = ['', 'rad', 'rad', '', '', '']
    mags_units = ['', '', '', '', '', '']
    units = basic_units + mags_units*2

    @staticmethod
    def get_column_outputs(bandname):
        return ['id', 'raJ2000', 'decJ2000',
                'lsst_'+bandname,
                'delta_lsst_'+bandname,
                #'sigma_lsst_'+bandname,
                'varParamStr']

class DiaSourceVarStars(DiaSourceCommons, BasicVarStars):

    catalog_type = 'variable_stars_dia'
    column_outputs = (DiaSourceCommons.column_outputs
            + BasicVarStars.total_mags + BasicVarStars.delta_mags)
    #column_outputs = DiaSourceCommons.column_outputs
    ucds = DiaSourceCommons.ucds + BasicVarStars.mags_ucds*2
    #ucds = DiaSourceCommons.ucds
    datatypes = DiaSourceCommons.datatypes + BasicVarStars.mags_datatypes*2
    units = DiaSourceCommons.units + BasicVarStars.mags_units*2

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
