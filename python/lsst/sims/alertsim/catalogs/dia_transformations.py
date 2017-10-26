""" dia_transformations """

import numpy as np
import re
import random

from lsst.sims.photUtils import Sed  # for converting magnitudes into fluxes
from lsst.sims.alertsim.catalogs.random_utils import array_to_dict

"""
A module which groups methods for transformation of catsim values 
to diaSource attributes as stated in DPDD.
These methods needed to be separated from catalog classes 
because ad-hoc usage is required.
"""

def midPointTai(tai):
    """
    Return mid point of exposure by taking OpSim start-of-exposure time
    and adding 17 seconds (15 seconds for first exposure; 1 second for
    shutter close; one second for shutter open).  Ignore the fact that,
    as DPDD states, midpoint will vary for different objects based on
    their position relative to the shutter motion.
    """
    return tai+17.0/86400.0


def ccdVisitId(obsHistID, chipNum):
    """
    Previous solution:
    Return chipNum*10^7 + obsHistID (obsHistID should never be more than 3 million)
    This was no good as 0220 was same as 2200
    Now:
    Return obsHistID*10^4 + chipNum
    """
    return obsHistID*10000+chipNum

def chipNum(chip_name):
    """
    Concatenate the digits in 'R:i,j S:m,n' to make the chip number ijmn
    """
    """
    for idx, val in enumerate(chip_name):
        if val is None: chip_name[idx] = '0'
        
    chip_arr = np.array([int(''.join(re.findall(r'\d+', name))) for name in chip_name])
    return chip_arr
    """
    return np.array([int(''.join(re.findall(r'\d+', name))) if name is not None else 0
                     for name in chip_name])

def diaSourceId(uniqueId, obsHistID):
    """
    A unique identifier for each DIASource (this needs to be unique for
    each apparition of a given object)

    Take uniqueID, multiply by 10^7 and add obsHistID from self.obs_metadata
    (obsHistID should only go up to about 3 million)
    """
    return uniqueId*10000000 + obsHistID

def fluxFromMag(mag):
    """
    Use Sed to convert mag into flux
    """
    ss = Sed()
    return ss.fluxFromMag(mag)

def fluxError(mean_mag_error, tot_mag_error, mean_flux, tot_flux):
    """
    The error in our measurement of the difference image flux.

    Note, we have assumed that
    magnitude_error = 2.5*log10(1 + 1/SNR)
    to get from magnitude errors to SNR
    """

    mean_snr = 1.0/(np.power(10.0, 0.4*mean_mag_error) - 1.0)
    tot_snr = 1.0/(np.power(10.0, 0.4*tot_mag_error) - 1.0)
    tot_flux_err = tot_flux/tot_snr
    mean_flux_err = mean_flux/mean_snr
    return np.array([np.sqrt(tot_flux_err*tot_flux_err + mean_flux_err*mean_flux_err),
                     tot_flux_err, mean_flux_err])

def snr(diaFlux, diaFluxError):
    """
    Get the SNR by dividing flux by uncertainty
    """
    return diaFlux/diaFluxError

def apFlux(diaFlux):
    """
    apMeanSb01 will be the true flux of the source.

    All others will be apMeanSb01 multiplied by 1.0 + epsilon,
    since CatSim does not contain methods to calculate different
    types of flux.
    """
    true_flux = diaFlux
    vals = np.array([true_flux,
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random()),
                     true_flux*(1.0+0.0001*random.random())]).T

    cols = ['apMeanSb01', 'apMeanSb02', 'apMeanSb03', 
             'apMeanSb04', 'apMeanSb05', 'apMeanSb06', 
             'apMeanSb07', 'apMeanSb08', 'apMeanSb09', 
             'apMeanSb10']
    
    return array_to_dict(cols, vals)

def apFluxErr(diaFluxError):
    """
    Calculate the true flux error by getting the magntidue error and assuming that

    magnitude_error = 2.5*log10(1 + 1/SNR)

    apMeanSb01Sigma will be the true flux error.  Everything else will be true flux error
    multiplied by 1+epsilon because CatSim does not have methods to calculate different types
    of fluxes.
    """
    true_fluxError = diaFluxError

    vals = np.array([true_fluxError,
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random()),
                     true_fluxError*(1.0+0.0001*random.random())]).T

    cols = ['apMeanSb01Err', 'apMeanSb02Err', 'apMeanSb03Err', 
             'apMeanSb04Err', 'apMeanSb05Err', 'apMeanSb06Err', 
             'apMeanSb07Err', 'apMeanSb08Err', 'apMeanSb09Err', 
             'apMeanSb10Err']
    
    return array_to_dict(cols, vals)

#def addEpsilon(some_value):
#    """
#    Add a small random epsilon to a value. Used for varieties of fluxes and errors 
#    which cannot be calculated at this moment
#    """
#    return some_value + 0.0001*random.random()

