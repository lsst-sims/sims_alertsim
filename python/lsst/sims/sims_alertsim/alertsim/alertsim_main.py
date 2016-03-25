""" Main module """

import subprocess
import time
from dataModel import DataMetadata, CelestialObject
from generateVOEvent import VOEventGenerator
import catsim_utils, opsim_utils
from lsst.sims.sims_alertsim.broadcast import *
from lsst.sims.sims_alertsim.catalogs import *

def main(opsim_table, catsim_table, opsim_constraint, 
         catsim_constraint, catalog, radius, protocol, ipaddr, port, header):

    """ Takes input args from cmd line parser or other,  
        query opsim, catsim, generate 
        and broadcast VOEvents 
    """

    print "Sims version: %s" % _get_sims_version() 

    sender = get_sender(protocol, ipaddr, port, header)
    
    observations = opsim_utils.opsim_query(stack_version = 10), 
            objid=opsim_table, constraint=opsim_constraint)
    for obs in observations:
        obs_data, obs_metadata = catsim_utils.catsim_query(stack_version = 10), 
                objid=catsim_table, constraint=catsim_constraint, 
                catalog=catalog, radius=radius, opsim_metadata=obs)
        #print vars(obs_metadata)
        iter_and_send(sender, obs_data, obs_metadata)
    
    sender.close()

def get_sender(protocol, ipaddr, port, header):
    """ Instantiate proper child class for the protocol """
    return vars(broadcast)[protocol](ipaddr, port, header)

def iter_and_send(sender, obs_data, obs_metadata):
    """ Iterate over catalog and generate XML """
    count = 0
    sending_times = []

    for line in obs_data.iter_catalog():
        data_metadata = []
        for (val, ucd, unit) in zip(line, 
                obs_data.get_ucds(), obs_data.get_units()):
            data_metadata.append(DataMetadata(val, ucd, unit))
        celestial_object = CelestialObject(obs_data.iter_column_names(), 
                data_metadata)
        gen = VOEventGenerator(eventid = count)
        xml = gen.generateFromObjects(celestial_object, obs_metadata)
        sender.send(xml)
        count = count + 1
        sending_times.append(time.time())

    sending_diff = sending_times[-1] - sending_times[0]
    print "Number of events from this visit : %d. Time from first to last " \
       "event %f or %f per event" % (count, sending_diff, sending_diff/count)


def _get_stack_version(fine_grain=True):
    """ ask eups for stack version, return in 2 flavors """
    # shell eups command to get version like 8.0.0.2
    # how to get version without eups?

    # now obsolete for time being

    stack_version = subprocess.check_output("eups list lsst --version " \
            "--tag current", shell=True)
    if fine_grain:
        return stack_version
    else:
        return int(stack_version.split('.')[0])

def _get_sims_version():
    return subprocess.check_output("eups list lsst --version " \
            "--tag current", shell=True)
