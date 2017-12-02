""" DiaSourceCommons """
import numpy as np
import re
from lsst.sims.alertsim.catalogs.random_utils import array_to_dict
from lsst.sims.catalogs.definitions import InstanceCatalog
from lsst.sims.catalogs.decorators import cached, compound
from lsst.sims.catUtils.mixins import CameraCoords
from lsst.sims.photUtils import Sed  # for converting magnitudes into fluxes
from lsst.obs.lsstSim import LsstSimMapper
from lsst.sims.coordUtils import lsst_camera

class DIAObjectCommons(CameraCoords):

    """ Common methods and attributes for all classes 
    which represent diaobject.
    Daughter classes will need to override some methods 
    depending of their variability model
    """

    # DIAObject columns as of DPDD from May 6th 2016

    
    """
    differences between DPDD and L1 schema
    N = Ndata
    """

    _seed = None
    _rng =None

    column_outputs = ['diaObjectId', 'ra', 'decl', 'ra_decl_Cov', 'radecTai', 'pmRa', 'pmDecl', 'parallax', 'pm_parallax_Cov', 'pmParallaxLnL', 'pmParallaxChi2', 'pmParallaxNdata', 'uPSFluxMean', 'uPSFluxMeanErr', 'uPSFluxSigma', 'uPSFluxChi2', 'uPSFluxNdata', 'gPSFluxMean', 'gPSFluxMeanErr', 'gPSFluxSigma', 'gPSFluxChi2', 'gPSFluxNdata', 'rPSFluxMean', 'rPSFluxMeanErr', 'rPSFluxSigma', 'rPSFluxChi2', 'rPSFluxNdata', 'iPSFluxMean', 'iPSFluxMeanErr', 'iPSFluxSigma', 'iPSFluxChi2', 'iPSFluxNdata', 'zPSFluxMean', 'zPSFluxMeanErr', 'zPSFluxSigma', 'zPSFluxChi2', 'zPSFluxNdata', 'yPSFluxMean', 'yPSFluxMeanErr', 'yPSFluxSigma', 'yPSFluxChi2', 'yPSFluxNdata', 'uFPFluxMean', 'uFPFluxMeanErr', 'uFPFluxSigma', 'gFPFluxMean', 'gFPFluxMeanErr', 'gFPFluxSigma', 'rFPFluxMean', 'rFPFluxMeanErr', 'rFPFluxSigma', 'iFPFluxMean', 'iFPFluxMeanErr', 'iFPFluxSigma', 'zFPFluxMean', 'zFPFluxMeanErr', 'zFPFluxSigma', 'yFPFluxMean', 'yFPFluxMeanErr', 'yFPFluxSigma', 'uLcPeriodic', 'gLcPeriodic', 'rLcPeriodic', 'iLcPeriodic', 'zLcPeriodic', 'yLcPeriodic', 'uLcNonPeriodic', 'gLcNonPeriodic', 'rLcNonPeriodic', 'iLcNonPeriodic', 'zLcNonPeriodic', 'yLcNonPeriodic', 'nearbyObj1', 'nearbyObj1Dist', 'nearbyObj1LnP', 'nearbyObj2', 'nearbyObj2Dist', 'nearbyObj2LnP', 'nearbyObj3', 'nearbyObj3Dist', 'nearbyObj3LnP', 'flags']

    # UCD's - TODO

    ucds = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

    # Datatypes as stated in DPDD TODO

    datatypes = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

    # Units as stated in DPDD TODO

    units = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

    # DIASource attributes with randomly assigned values (for the time being)

    def write_catalog(self, *args, **kwargs):
        raise NotImplementedError("You cannot call write_catalog() on "
                                  "VariableStarsDia; write_catalog() does not "
                                  "know how to deal with the nested structure "
                                  "of the DIASource schema")
     
    # the software representation of the LSST camera
    camera = lsst_camera()

    # getters for DIASource attributes which are generated from catsim

    @property
    def rng(self):
        """
        A random number generator for the catalog.
        It is seeded by the self._seed parameter.
        If self._seed is None (default), then rng
        is seeded from the system clock as per numpy's
        default.
        """
        if self._rng is None:
            self._rng = np.random.RandomState(self._seed)
        return self._rng

    def randomFloats(self, n_obj):
        """
        Return a list of random floats between 0 and 1.0
        that is n_obj long.

        If n_obj<0, get n_obj from the length of another
        column in the catalog
        """
        if n_obj < 0:
            n_obj = len(self.column_by_name('chipNum'))

        if n_obj == 0:
            return np.array([])

        return self.rng.random_sample(n_obj)

    def randomFloatArr(self, n_rows, n_cols):
        """
        Return a 2-D array of random floats between 0 and 1.0.
        The array will be n_rows by n_cols.
        If one of the dimensin is less than 0, it will be set
        to the number of rows in the catalog.
        """
        if n_rows < 0:
            n_rows = len(self.column_by_name('chipNum'))
        if n_cols < 0:
            n_cols = len(self.column_by_name('chipNum'))

        if n_cols == 0:
            return np.array([[]]*n_cols)
        if n_rows == 0:
            return np.array([])

        return self.rng.random_sample((n_rows, n_cols)).transpose()

    def randomInts(self, n_obj, i_max=1000):
        """
        Return a list of n_obj random integers between
        zero and i_max (inclusive)

        If n_obj<0, get n_obj from the length of another
        column in the catalog
        """
        if n_obj < 0:
            n_obj = len(self.column_by_name('chipNum'))

        if n_obj == 0:
            return np.array([])
        return self.rng.randint(0,i_max,n_obj)

##################
    # diaObjectId
    # ra
    # decl
    # 
    def get_ra_decl_Cov(self):
	vals = self.randomFloatArr(3, -1)
	cols = ['raSigma','declSigma','ra_decl_Cov']
	return array_to_dict(cols, vals)    

    def get_radecTai(self):
	return self.randomFloats(-1)

    def get_pmRa(self):
	return self.randomFloats(-1)
    
    def get_pmDecl(self):
	return self.randomFloats(-1)
    
    def get_parallax(self):
	return self.randomFloats(-1)
    
    def get_pm_parallax_Cov(self):
	vals = self.randomFloatArr(6, -1)
	cols = ['pmRaSigma', 'pmDeclSigma', 'parallaxSigma', 'pmRa_pmDecl_Cov', 'pmRa_parallax_Cov', 'pmDecl_parallax_Cov']
	return array_to_dict(cols, vals)
    
    def get_pmParallaxLnL(self):
	return self.randomFloats(-1)
    
    def get_pmParallaxChi2(self):
	return self.randomFloats(-1)
    
    def get_pmParallaxNdata(self):
	return self.randomFloats(-1)
    
    def get_uPSFluxMean(self):
	return self.randomFloats(-1)
    
    def get_uPSFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_uPSFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_uPSFluxChi2(self):
	return self.randomFloats(-1)
    
    def get_uPSFluxNdata(self):
	return self.randomFloats(-1)
    
    def get_gPSFluxMean(self):
	return self.randomFloats(-1)
    
    def get_gPSFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_gPSFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_gPSFluxChi2(self):
	return self.randomFloats(-1)
    
    def get_gPSFluxNdata(self):
	return self.randomFloats(-1)
    
    def get_rPSFluxMean(self):
	return self.randomFloats(-1)
    
    def get_rPSFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_rPSFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_rPSFluxChi2(self):
	return self.randomFloats(-1)
    
    def get_rPSFluxNdata(self):
	return self.randomFloats(-1)
    
    def get_iPSFluxMean(self):
	return self.randomFloats(-1)
    
    def get_iPSFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_iPSFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_iPSFluxChi2(self):
	return self.randomFloats(-1)
    
    def get_iPSFluxNdata(self):
	return self.randomFloats(-1)
    
    def get_zPSFluxMean(self):
	return self.randomFloats(-1)
    
    def get_zPSFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_zPSFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_zPSFluxChi2(self):
	return self.randomFloats(-1)
    
    def get_zPSFluxNdata(self):
	return self.randomFloats(-1)
    
    def get_yPSFluxMean(self):
	return self.randomFloats(-1)
    
    def get_yPSFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_yPSFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_yPSFluxChi2(self):
	return self.randomFloats(-1)
    
    def get_yPSFluxNdata(self):
	return self.randomFloats(-1)
    
    def get_uFPFluxMean(self):
	return self.randomFloats(-1)
    
    def get_uFPFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_uFPFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_gFPFluxMean(self):
	return self.randomFloats(-1)
    
    def get_gFPFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_gFPFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_rFPFluxMean(self):
	return self.randomFloats(-1)
    
    def get_rFPFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_rFPFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_iFPFluxMean(self):
	return self.randomFloats(-1)
    
    def get_iFPFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_iFPFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_zFPFluxMean(self):
	return self.randomFloats(-1)
    
    def get_zFPFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_zFPFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_yFPFluxMean(self):
	return self.randomFloats(-1)
    
    def get_yFPFluxMeanErr(self):
	return self.randomFloats(-1)
    
    def get_yFPFluxSigma(self):
	return self.randomFloats(-1)
    
    def get_uLcPeriodic(self):
	vals = self.randomFloatArr(32, -1)
	cols = ['uLcPeriodic01', 'uLcPeriodic02', 'uLcPeriodic03', 'uLcPeriodic04', 'uLcPeriodic05', 'uLcPeriodic06', 'uLcPeriodic07', 'uLcPeriodic08', 'uLcPeriodic09', 'uLcPeriodic10', 'uLcPeriodic11', 'uLcPeriodic12', 'uLcPeriodic13', 'uLcPeriodic14', 'uLcPeriodic15', 'uLcPeriodic16', 'uLcPeriodic17', 'uLcPeriodic18', 'uLcPeriodic19', 'uLcPeriodic20', 'uLcPeriodic21', 'uLcPeriodic22', 'uLcPeriodic23', 'uLcPeriodic24', 'uLcPeriodic25', 'uLcPeriodic26', 'uLcPeriodic27', 'uLcPeriodic28', 'uLcPeriodic29', 'uLcPeriodic30', 'uLcPeriodic31', 'uLcPeriodic32']
	return array_to_dict(cols, vals)

    def get_gLCPeriodic(self):
	vals = self.randomFloatArr(32, -1)
	cols = ['gLCPeriodic01', 'gLCPeriodic02', 'gLCPeriodic03', 'gLCPeriodic04', 'gLCPeriodic05', 'gLCPeriodic06', 'gLCPeriodic07', 'gLCPeriodic08', 'gLCPeriodic09', 'gLCPeriodic10', 'gLCPeriodic11', 'gLCPeriodic12', 'gLCPeriodic13', 'gLCPeriodic14', 'gLCPeriodic15', 'gLCPeriodic16', 'gLCPeriodic17', 'gLCPeriodic18', 'gLCPeriodic19', 'gLCPeriodic20', 'gLCPeriodic21', 'gLCPeriodic22', 'gLCPeriodic23', 'gLCPeriodic24', 'gLCPeriodic25', 'gLCPeriodic26', 'gLCPeriodic27', 'gLCPeriodic28', 'gLCPeriodic29', 'gLCPeriodic30', 'gLCPeriodic31', 'gLCPeriodic32']
	return array_to_dict(cols, vals)

    def get_rLcPeriodic(self):
	vals = self.randomFloatArr(32, -1)
	cols = ['rLcPeriodic01', 'rLcPeriodic02', 'rLcPeriodic03', 'rLcPeriodic04', 'rLcPeriodic05', 'rLcPeriodic06', 'rLcPeriodic07', 'rLcPeriodic08', 'rLcPeriodic09', 'rLcPeriodic10', 'rLcPeriodic11', 'rLcPeriodic12', 'rLcPeriodic13', 'rLcPeriodic14', 'rLcPeriodic15', 'rLcPeriodic16', 'rLcPeriodic17', 'rLcPeriodic18', 'rLcPeriodic19', 'rLcPeriodic20', 'rLcPeriodic21', 'rLcPeriodic22', 'rLcPeriodic23', 'rLcPeriodic24', 'rLcPeriodic25', 'rLcPeriodic26', 'rLcPeriodic27', 'rLcPeriodic28', 'rLcPeriodic29', 'rLcPeriodic30', 'rLcPeriodic31', 'rLcPeriodic32']
	return array_to_dict(cols, vals)

    def get_iLcPeriodic(self):
	vals = self.randomFloatArr(32, -1)
	cols = ['iLcPeriodic01', 'iLcPeriodic02', 'iLcPeriodic03', 'iLcPeriodic04', 'iLcPeriodic05', 'iLcPeriodic06', 'iLcPeriodic07', 'iLcPeriodic08', 'iLcPeriodic09', 'iLcPeriodic10', 'iLcPeriodic11', 'iLcPeriodic12', 'iLcPeriodic13', 'iLcPeriodic14', 'iLcPeriodic15', 'iLcPeriodic16', 'iLcPeriodic17', 'iLcPeriodic18', 'iLcPeriodic19', 'iLcPeriodic20', 'iLcPeriodic21', 'iLcPeriodic22', 'iLcPeriodic23', 'iLcPeriodic24', 'iLcPeriodic25', 'iLcPeriodic26', 'iLcPeriodic27', 'iLcPeriodic28', 'iLcPeriodic29', 'iLcPeriodic30', 'iLcPeriodic31', 'iLcPeriodic32']
	return array_to_dict(cols, vals)

    def get_zLcPeriodic(self):
	vals = self.randomFloatArr(32, -1)
	cols = ['zLcPeriodic01', 'zLcPeriodic02', 'zLcPeriodic03', 'zLcPeriodic04', 'zLcPeriodic05', 'zLcPeriodic06', 'zLcPeriodic07', 'zLcPeriodic08', 'zLcPeriodic09', 'zLcPeriodic10', 'zLcPeriodic11', 'zLcPeriodic12', 'zLcPeriodic13', 'zLcPeriodic14', 'zLcPeriodic15', 'zLcPeriodic16', 'zLcPeriodic17', 'zLcPeriodic18', 'zLcPeriodic19', 'zLcPeriodic20', 'zLcPeriodic21', 'zLcPeriodic22', 'zLcPeriodic23', 'zLcPeriodic24', 'zLcPeriodic25', 'zLcPeriodic26', 'zLcPeriodic27', 'zLcPeriodic28', 'zLcPeriodic29', 'zLcPeriodic30', 'zLcPeriodic31', 'zLcPeriodic32']
	return array_to_dict(cols, vals)

    def get_yLcPeriodic(self):
	vals = self.randomFloatArr(32, -1)
	cols = ['yLcPeriodic01', 'yLcPeriodic02', 'yLcPeriodic03', 'yLcPeriodic04', 'yLcPeriodic05', 'yLcPeriodic06', 'yLcPeriodic07', 'yLcPeriodic08', 'yLcPeriodic09', 'yLcPeriodic10', 'yLcPeriodic11', 'yLcPeriodic12', 'yLcPeriodic13', 'yLcPeriodic14', 'yLcPeriodic15', 'yLcPeriodic16', 'yLcPeriodic17', 'yLcPeriodic18', 'yLcPeriodic19', 'yLcPeriodic20', 'yLcPeriodic21', 'yLcPeriodic22', 'yLcPeriodic23', 'yLcPeriodic24', 'yLcPeriodic25', 'yLcPeriodic26', 'yLcPeriodic27', 'yLcPeriodic28', 'yLcPeriodic29', 'yLcPeriodic30', 'yLcPeriodic31', 'yLcPeriodic32']
	return array_to_dict(cols, vals)

    def get_uLcNonPeriodic(self):
	vals = self.randomFloatArr(20, -1)
	cols = ['uLcNonPeriodic01', 'uLcNonPeriodic02', 'uLcNonPeriodic03', 'uLcNonPeriodic04', 'uLcNonPeriodic05', 'uLcNonPeriodic06', 'uLcNonPeriodic07', 'uLcNonPeriodic08', 'uLcNonPeriodic09', 'uLcNonPeriodic10', 'uLcNonPeriodic11', 'uLcNonPeriodic12', 'uLcNonPeriodic13', 'uLcNonPeriodic14', 'uLcNonPeriodic15', 'uLcNonPeriodic16', 'uLcNonPeriodic17', 'uLcNonPeriodic18', 'uLcNonPeriodic19', 'uLcNonPeriodic20']
	return array_to_dict(cols, vals)

    def get_gLcNonPeriodic(self):
	vals = self.randomFloatArr(20, -1)
	cols = ['gLcNonPeriodic01', 'gLcNonPeriodic02', 'gLcNonPeriodic03', 'gLcNonPeriodic04', 'gLcNonPeriodic05', 'gLcNonPeriodic06', 'gLcNonPeriodic07', 'gLcNonPeriodic08', 'gLcNonPeriodic09', 'gLcNonPeriodic10', 'gLcNonPeriodic11', 'gLcNonPeriodic12', 'gLcNonPeriodic13', 'gLcNonPeriodic14', 'gLcNonPeriodic15', 'gLcNonPeriodic16', 'gLcNonPeriodic17', 'gLcNonPeriodic18', 'gLcNonPeriodic19', 'gLcNonPeriodic20']
	return array_to_dict(cols, vals)

    def get_rLcNonPeriodic(self):
	vals = self.randomFloatArr(20, -1)
	cols = ['rLcNonPeriodic01', 'rLcNonPeriodic02', 'rLcNonPeriodic03', 'rLcNonPeriodic04', 'rLcNonPeriodic05', 'rLcNonPeriodic06', 'rLcNonPeriodic07', 'rLcNonPeriodic08', 'rLcNonPeriodic09', 'rLcNonPeriodic10', 'rLcNonPeriodic11', 'rLcNonPeriodic12', 'rLcNonPeriodic13', 'rLcNonPeriodic14', 'rLcNonPeriodic15', 'rLcNonPeriodic16', 'rLcNonPeriodic17', 'rLcNonPeriodic18', 'rLcNonPeriodic19', 'rLcNonPeriodic20']
	return array_to_dict(cols, vals)

    def get_iLcNonPeriodic(self):
	vals = self.randomFloatArr(20, -1)
	cols = ['iLcNonPeriodic01', 'iLcNonPeriodic02', 'iLcNonPeriodic03', 'iLcNonPeriodic04', 'iLcNonPeriodic05', 'iLcNonPeriodic06', 'iLcNonPeriodic07', 'iLcNonPeriodic08', 'iLcNonPeriodic09', 'iLcNonPeriodic10', 'iLcNonPeriodic11', 'iLcNonPeriodic12', 'iLcNonPeriodic13', 'iLcNonPeriodic14', 'iLcNonPeriodic15', 'iLcNonPeriodic16', 'iLcNonPeriodic17', 'iLcNonPeriodic18', 'iLcNonPeriodic19', 'iLcNonPeriodic20']
	return array_to_dict(cols, vals)

    def get_zLcNonPeriodic(self):
	vals = self.randomFloatArr(20, -1)
	cols = ['zLcNonPeriodic01', 'zLcNonPeriodic02', 'zLcNonPeriodic03', 'zLcNonPeriodic04', 'zLcNonPeriodic05', 'zLcNonPeriodic06', 'zLcNonPeriodic07', 'zLcNonPeriodic08', 'zLcNonPeriodic09', 'zLcNonPeriodic10', 'zLcNonPeriodic11', 'zLcNonPeriodic12', 'zLcNonPeriodic13', 'zLcNonPeriodic14', 'zLcNonPeriodic15', 'zLcNonPeriodic16', 'zLcNonPeriodic17', 'zLcNonPeriodic18', 'zLcNonPeriodic19', 'zLcNonPeriodic20']
	return array_to_dict(cols, vals)

    def get_yLcNonPeriodic(self):
	vals = self.randomFloatArr(20, -1)
	cols = ['yLcNonPeriodic01', 'yLcNonPeriodic02', 'yLcNonPeriodic03', 'yLcNonPeriodic04', 'yLcNonPeriodic05', 'yLcNonPeriodic06', 'yLcNonPeriodic07', 'yLcNonPeriodic08', 'yLcNonPeriodic09', 'yLcNonPeriodic10', 'yLcNonPeriodic11', 'yLcNonPeriodic12', 'yLcNonPeriodic13', 'yLcNonPeriodic14', 'yLcNonPeriodic15', 'yLcNonPeriodic16', 'yLcNonPeriodic17', 'yLcNonPeriodic18', 'yLcNonPeriodic19', 'yLcNonPeriodic20']
	return array_to_dict(cols, vals)
    
    def get_nearbyObj1(self):
	return self.randomInts(-1, 9223372036854775807)
    
    def get_nearbyObj1Dist(self):
	return self.randomFloats(-1)
    
    def get_nearbyObj1LnP(self):
	return self.randomFloats(-1)
    
    def get_nearbyObj2(self):
	return self.randomInts(-1, 9223372036854775807)
    
    def get_nearbyObj2Dist(self):
	return self.randomFloats(-1)
    
    def get_nearbyObj2LnP(self):
	return self.randomFloats(-1)
    
    def get_nearbyObj3(self):
	return self.randomInts(-1, 9223372036854775807)
    
    def get_nearbyObj3Dist(self):
	return self.randomFloats(-1)
    
    def get_nearbyObj3LnP(self):
	return self.randomFloats(-1)
