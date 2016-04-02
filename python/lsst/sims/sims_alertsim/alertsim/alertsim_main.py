""" Main module """
# 
# Boilerplate
# 

import subprocess
import time
from dataModel import DataMetadata, CelestialObject
from generateVOEvent import VOEventGenerator
import catsim_utils, opsim_utils
from lsst.sims.sims_alertsim.broadcast import *
from lsst.sims.sims_alertsim.catalogs import *

def main(opsim_table, catsim_table, opsim_constraint, 
         catsim_constraint, catalog, radius, protocol, ipaddr, port, header):

    """ Take input args from cmd line parser or other,  
        query opsim and get observations,
        for each observation, query catsim and get celestial objects,
        for each celestial object, generate and broadcast VOEvents.
        
    Parameters
    ----------
    opsim_table : str
        opsim objid, e.g. "output_opsim3_61"
    catsim_table : str
        catsim objid, e.g. "allstars"
    opsim_constraint : str
        constraint for opsim query, e.g. "(night=10 and rawseeing<0.6) and filter like \'i\' "
    catsim_constraint : str
        constraint for catsim query, e.g. "rmag between 20 and 23.5"
    catalog : str
        name of catsim catalog, choices=["variable_stars", "vanilla_stars", "DIA_sources", "DIA_objects"]
    radius : float
        cone search radius, e.g. 0.05
    protocol : str
        protocol (TcpIp, Multicast, Unicast)
    ipaddr : str
        ip address of the recepient or multicast channel
    port : int
        tcp port
    header : bool
        ????
        
    """

    print "Sims version: %s" % _get_sims_version() 

    sender = get_sender(protocol, ipaddr, port, header)
    
    observations = opsim_utils.opsimQuery(stack_version=10, 
            objid=opsim_table, constraint=opsim_constraint)
    for obs in observations:
        obs_data, obs_metadata = catsim_utils.catsimQuery(stack_version=10, 
                objid=catsim_table, constraint=catsim_constraint, 
                catalog=catalog, radius=radius, opsim_metadata=obs)
        #print vars(obs_metadata)
        iter_and_send(sender, obs_data, obs_metadata)
    
    sender.close()

def get_sender(protocol, ipaddr, port, header):
    """ Instantiate proper child class for the protocol """
    return vars(broadcast)[protocol](ipaddr, port, header)

def iter_and_send(sender, obs_data, obs_metadata):
    """ Iterate over catalog and generate XML
    
    Parameters
    ----------
    sender : 
        Sender of alerts, e.g. TcpIp object
    obs_data : 
        Data of observed object. Contains ra, dec and other data, depending of catalog type,
        defined in catalogExamples. e.g. VariableStars object
    obs_metadata : ObservationMetaData object
        Data describing observation (filter, mjd, ...)
    """
    
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
    return subprocess.check_output("eups list lsst_sims --version " \
            "--tag current", shell=True)
