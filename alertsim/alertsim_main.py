""" Parse input args and broadcast VOEvents """

import sys
import subprocess
from dataModel import DataMetadata, CelestialObject
from generateVOEvent import VOEventGenerator
import catsim_utils, opsim_utils
from broadcast import *
from catalogs import *

def main(opsim_table, catsim_table, opsim_constraint, 
         catsim_constraint, catalog, radius, protocol, ipaddr, port, header):

    """ Take objids, constraints and metadata, query
        opsim and catsim and generate VOevents 
    """

    print "Stack version: %s" % get_stack_version() 

    sender = get_sender(protocol, ipaddr, port, header)
    
    observations = opsim_utils.opsim_query(get_stack_version(fine_grain=False), objid=opsim_table, 
                constraint=opsim_constraint)
    for obs in observations:
        t, obs_metadata = catsim_utils.catsim_query(get_stack_version(fine_grain=False), objid=catsim_table, constraint=catsim_constraint, 
                    catalog=catalog, radius=radius, opsim_metadata=obs)
        iter_and_send(sender, t, obs_metadata)
    
    sender.close()

def get_sender(protocol, ipaddr, port, header):
    """ Instantiate proper child class for the protocol """
    return vars(broadcast)[protocol](ipaddr, port, header)

def iter_and_send(sender, t, obs_metadata):
    """ Iterate over catalog and generate XML """
    count = 0

    for line in t.iter_catalog():
        dataMetadata = []
        for (val, ucd, unit) in zip(line, t.get_ucds(), t.get_units()):
            dataMetadata.append(DataMetadata(val, ucd, unit))
        c = CelestialObject(t.iter_column_names(), dataMetadata)
        gen = VOEventGenerator(eventid = count)
        xml = gen.generateFromObjects(c, obs_metadata)
        sender.send(xml)
        count = count + 1

    print "Number of events from this visit : %s" % count

def get_stack_version(fine_grain=True):
    # shell eups command to get version like 8.0.0.2
    # how to get version without eups?
    stack_version = subprocess.check_output("eups list lsst --version --tag current", shell=True)
    if fine_grain:
        return stack_version
    else:
        return int(stack_version.split('.')[0])
