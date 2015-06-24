"""Instance Catalog"""
import numpy
import eups
from lsst.sims.catalogs.measures.instance import InstanceCatalog
from lsst.sims.coordUtils.Astrometry import AstrometryStars, CameraCoords
from lsst.sims.photUtils.Photometry import PhotometryStars
from lsst.obs.lsstSim.utils import loadCamera
from lsst.sims.photUtils.Variability import Variability, VariabilityStars

class VariableStars(InstanceCatalog,PhotometryStars,VariabilityStars):

    """
    def __init__(self, band):
        column_outputs += [band, band + '_var']
    """
    
    catalog_type = 'variable_stars'
    """
    column_outputs = ['id','raJ2000','decJ2000',
                      'lsst_u','lsst_g','lsst_r','lsst_i','lsst_z','lsst_y',
                      'delta_lsst_u','delta_lsst_g','delta_lsst_i','delta_lsst_z',
                      'delta_lsst_y']
    """
    column_outputs = ['id','raJ2000','decJ2000',
                      'lsst_u','lsst_g','lsst_r','lsst_i','lsst_z','lsst_y',
                      'lsst_u_var','lsst_g_var','lsst_i_var','lsst_z_var',
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
