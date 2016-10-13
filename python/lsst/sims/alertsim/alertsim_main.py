""" Main module """

import subprocess
import sys
import time
import functools
import catsim_utils, opsim_utils
#import threading
#import itertools
from copy import deepcopy
from lsst.sims.alertsim.dataModel import DataMetadata, CelestialObject
from lsst.sims.alertsim.generateVOEvent import VOEventGenerator
from lsst.sims.alertsim.broadcast import *
from lsst.sims.alertsim.catalogs import *

BANDNAMES = ['u', 'g', 'r', 'i', 'z', 'y']
STACK_VERSION = 10

def main(opsim_table, catsim_table, opsim_constraint, 
         catsim_constraint, radius, protocol, ipaddr, 
         port, header, history, dia):

    """ Takes input args from cmd line parser or other,  
        query opsim, catsim, generate 
        and broadcast VOEvents 
    """

    sender = get_sender(protocol, ipaddr, port, header)
    
    print "fetching opsim results..."
    
    # keeping this for now, will try to build a thread-based spinner 
    # for db queries as they can last quite a bit
    """
    obs_all = []
    t1 = threading.Thread(target = thread_wrapper, 
            args = (opsim_utils.opsim_query, 
                (stack_version=STACK_VERSION, objid=opsim_table, 
                    radius=radius, constraint=opsim_constraint), obs_all))
    
    while t1.is_alive():
        sys.stdout.write(spinner.next())  # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')            # erase the last written char
        t1.join(0.2)
    """

    """ matrix of all observations per field up to current mjd """
    obs_all = opsim_utils.opsim_query(stack_version=10, 
            objid=opsim_table, radius=radius, constraint=opsim_constraint)

    print "opsim result fetched and transformed to ObservationMetaData objects"

    for obs_per_field in obs_all:

        """ current observation - largest mjd from a sorted list  """
        obs_metadata = obs_per_field[0]
        
        obs_data = catsim_utils.catsim_query(stack_version=10, 
                objid=catsim_table, constraint=catsim_constraint, 
                obs_metadata=obs_metadata, dia=dia)

        iter_and_send(sender, obs_data, obs_metadata, obs_per_field, history)
    
    sender.close()

def get_sender(protocol, ipaddr, port, header):
    """ Instantiate proper child class for the protocol """
    return vars(broadcast)[protocol](ipaddr, port, header)

def iter_and_send(sender, obs_data, obs_metadata, observations_field, history):

    """ Iterate over catalog and generate XML """

    event_count = 0
    sending_times = []

    for line in obs_data.iter_catalog():

        # current + historical exposures
        cel_objects = []

        data_metadata = []
            
        # append metadata to each attribute
        for (val, ucd, unit) in zip(line, obs_data.ucds, 
                obs_data.units):
            data_metadata.append(DataMetadata(val, ucd, unit))

        # current exposure with all mags and deltas. 
        # will need it for calculating historical variability in 
        # different bands.

        cel_obj_all_mags = CelestialObject(obs_data.iter_column_names(), 
                data_metadata)
        
        if (cel_obj_all_mags.varParamStr.value == 'None'):
            print "You should declare varParamStr not like " \
                  "'None' in catsim constraint"
            exit(1)

        cel_obj = deepcopy(cel_obj_all_mags)
        
        # reduce to a single band
        _remove_band_attrs(cel_obj, obs_metadata.bandpass)
        cel_objects.append(cel_obj)

        # historical exposures can be turned off
        if history:
            
            base_mags = {}
            for band in BANDNAMES:
                # substract deltas from mags to get base for historical mags
                mag_attr = getattr(cel_obj_all_mags, 'lsst_'+band)
                delta_mag_attr = getattr(cel_obj_all_mags, 'delta_lsst_'+band)
                # other way would be to calculate historical mags 
                # via PhotometryStars. 
                base_mags[band] = mag_attr.value + delta_mag_attr.value

            for historical_metadata in observations_field:
                vs = VariabilityDummy(historical_metadata)

                # can we get filter-parametrized variabilities 
                # from VariabilityMixin please? 
                hist_delta_mags = vs.applyVariability(cel_obj_all_mags.varParamStr.value)
                hist_cel_obj = deepcopy(cel_obj_all_mags)

                # not optimal but most flexible for now
                for band in BANDNAMES:
                    hist_mag = base_mags[band] + hist_delta_mags[band] 
                    hist_delta_mag = hist_delta_mags[band]
                    _rsetattr(hist_cel_obj, 'lsst_'+band+'.value', hist_mag)
                    _rsetattr(hist_cel_obj, 'delta_lsst_'+band+'.value', 
                            hist_delta_mag)
                
                _remove_band_attrs(hist_cel_obj, historical_metadata.bandpass)
                cel_objects.append(hist_cel_obj)


        # generate and send
        gen = VOEventGenerator(eventid = event_count)
        xml = gen.generateFromObjects(cel_objects, obs_metadata)
        #print xml
        sender.send(xml)
        event_count += 1
        sending_times.append(time.time())

    print "sdada"
    # add exception for index out of range
    try:
        sending_diff = sending_times[-1] - sending_times[0]
        print "Number of events from this visit : %d. Time from first to last " \
            "event %f or %f per event" % (event_count, sending_diff, 
                    sending_diff/event_count)
    except IndexError:
        print "No events in this visit"


def _remove_band_attrs(obj, bandname):
    """ reduce object dictionary """
    # this may not be the safest way and needs to be revised
    for key in obj.__dict__.keys():
        if ('lsst' in key) and not (key.endswith(bandname)):
            obj.__dict__.pop(key)

"""
def _rename_band_attr(obj, bandname):
        for key in obj.__dict__:
            if 'lsst' in key:
                new_key = key[:-1] + bandname
                obj.__dict__[new_key] = obj.__dict__.pop(old_name)
"""

def _rsetattr(obj, attr, val):
    """ fix setattr lack of dot notation support """
    pre, _, post = attr.rpartition('.')
    return setattr(functools.reduce(getattr, 
        [obj]+pre.split('.')) if pre else obj, post, val)

"""
def thread_wrapper(func, args, res):
    res.append(func(*args))

def spinner():
    return itertools.cycle(['-', '/', '|', '\\'])
"""
