import numpy as np
from collections import OrderedDict
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catUtils.mixins import AstrometryStars, CameraCoords, PhotometryStars, Variability, VariabilityStars
from lsst.sims.catUtils.baseCatalogModels import *
from lsst.sims.catalogs.decorators import compound
from lsst.sims.alertsim.catalogs import DiaSourceCommons

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

class DiaSourceVarStars(DiaSourceCommons):

    catalog_type = 'variable_stars_dia'

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
