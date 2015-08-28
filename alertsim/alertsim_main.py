""" Parse input args and broadcast VOEvents """

import sys
import subprocess
from dataModel import DataMetadata, CelestialObject
from generateVOEvent import VOEventGenerator
import catsim_utils, opsim_utils, alert
from broadcast import *
from catalogs import *

def main(opsim_table, catsim_table, opsim_constraint, 
         catsim_constraint, catalog, radius, protocol, ipaddr, port, header):

    """ Take objids, constraints and metadata, query
        opsim and catsim and generate VOevents 
    """

    print "Stack version: %s" % get_stack_version() 

    sender = get_sender(protocol, ipaddr, port, header)
    
    # Query OpSim
    observations = opsim_utils.opsim_query(get_stack_version(fine_grain=False), objid=opsim_table, 
                constraint=opsim_constraint)
    
    # For each visit, query Catsim
    for visit in observations:
        observed_objects, obs_metadata = catsim_utils.catsim_query(get_stack_version(fine_grain=False), objid=catsim_table, constraint=catsim_constraint, 
                    catalog=catalog, radius=radius, opsim_metadata=visit)

        # For each object, obtain object data, then generate and process alert
        for line in observed_objects.iter_catalog():
	  dataMetadata = []
	  for (val, ucd, unit) in zip(line, observed_objects.get_ucds(), observed_objects.get_units()):
	    dataMetadata.append(DataMetadata(val, ucd, unit))
	  obj_data = CelestialObject(observed_objects.iter_column_names(), dataMetadata)  # TODO: obj_data.cutoutImage = None
	  
	  # Generate alert
	  alertObject = alert.Alert(obs_metadata, obj_data)
	  
	  # Send alert
	  alertObject.send(sender)
	  alertObject.setStatus("Sent")
	  
	  # Print infos
	  print "Alert ID:", alertObject.alertid, " Message size:", alertObject.getSize(), " Timestamp:", alertObject.timestamp, " Status:", alertObject.getStatus()
	  
	  # Postprocess
	  # analyze feedback, timestamps and status
	  
	  # Logging
	  # alertObject.writeToDatabase('alerts.db') # TODO: Works, but place open/close connections outside.

        
        print "Number of events from this visit : %s" % alertObject.currentIdNum
        alertObject.__class__.currentIdNum = 0

    
    sender.close()


def get_sender(protocol, ipaddr, port, header):
    """ Instantiate proper child class for the protocol """
    return vars(broadcast)[protocol](ipaddr, port, header)


def iter_and_print(observed_objects, obs_metadata):
    """ Iterate over catalog and generate XML """
    count = 0

    for line in observed_objects.iter_catalog():
        dataMetadata = [] # <alertsim.dataModel.DataMetadata object>
        for (val, ucd, unit) in zip(line, observed_objects.get_ucds(), observed_objects.get_units()):
            dataMetadata.append(DataMetadata(val, ucd, unit))
            # print val, ucd, unit
            # print zip(line, observed_objects.get_ucds(), observed_objects.get_units())
        obj_data = CelestialObject(observed_objects.iter_column_names(), dataMetadata) # <alertsim.dataModel.CelestialObject object>
        gen = VOEventGenerator(eventid = count)
        xml = gen.generateFromObjects(obj_data, obs_metadata)
        print xml
        # print obs_metadata.mjd, obs_metadata.bandpass, obs_metadata.obshistid  # 49363.05809 i 85163538 (ovaj poslednji se menja u svakoj grupi, tj. za svaki visit)
        # print line # tuple ; (820431291, 1.0672489024438163, -0.075943665257342044, 23.588583592804845, 21.164706700237513, 20.112325943160165, 19.680817183015602, 19.488111639337195, 19.38065421569986, 23.588583592804845, 21.164706700237513, 20.112325943160165, 19.680817183015602, 19.488111639337195, 19.38065421569986)
        # print obj_data.raJ2000, obj_data.decJ2000, obj_data.lsst_g, obj_data.lsst_g_var # <alertsim.dataModel.DataMetadata object> <alertsim.dataModel.DataMetadata object> <alertsim.dataModel.DataMetadata object> <alertsim.dataModel.DataMetadata object>
        
        count = count + 1

    print "Number of events from this visit : %s" % count


def iter_and_send(sender, observed_objects, obs_metadata):
    """ Iterate over catalog and generate XML """
    count = 0

    for line in observed_objects.iter_catalog():
        dataMetadata = []
        for (val, ucd, unit) in zip(line, observed_objects.get_ucds(), observed_objects.get_units()):
            dataMetadata.append(DataMetadata(val, ucd, unit))
        obj_data = CelestialObject(observed_objects.iter_column_names(), dataMetadata)
        gen = VOEventGenerator(eventid = count)
        xml = gen.generateFromObjects(obj_data, obs_metadata)
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
