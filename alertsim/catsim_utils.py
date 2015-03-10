""" Query catsim and use VOEventLib to generate XML """

from math import pi
from lsst.sims.catalogs.generation.db import DBObject, ObservationMetaData
from alertsim import *
from catalogs import *
from broadcast import *

def catsim_query(objid, constraint, catalog, radius, opsim_metadata):

    """ Query catsim and make a catalog """

    obs_metadata = ObservationMetaData(circ_bounds=dict
            (ra=opsim_metadata[1]*180/pi, 
                dec=opsim_metadata[2]*180/pi, 
                radius=radius),
            mjd=opsim_metadata[5])
    dbobj = DBObject.from_objid(objid)
    
    t = dbobj.getCatalog(catalog, 
            obs_metadata=obs_metadata, 
            constraint=constraint)
#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return t, obs_metadata

def iter_and_send(sender, t, obs_metadata):
    
    """ Iterate over catalog and generate XML """

    count = 0
    gen = VOEventGenerator()

    for line in t.iter_catalog():
        dataMetadata = []
        for (val, ucd, unit) in zip(line, t.get_ucds(), t.get_units()):
            dataMetadata.append(DataMetadata(val, ucd, unit))
        c = CelestialObject(t.iter_column_names(), dataMetadata)
        xml = gen.generateFromObjects(c, obs_metadata, eventID=count)
        sender.send(xml)
        count = count + 1
    print "Number of events from this visit : %s" % count

def get_sender(protocol, ipaddr, port):
    """ Determine sending protocol """
    return vars(broadcast)[protocol](ipaddr, port)

