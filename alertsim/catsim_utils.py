""" Query catsim """

from math import pi
from lsst.sims.catUtils.baseCatalogModels import *

def catsim_query(stack_version, **kwargs):

    """ Determine stack version """

    if stack_version < 10:
        return catsim_query_stack8(**kwargs)
    else:
        return catsim_query_stack10(**kwargs)


def catsim_query_stack8(objid, constraint, catalog, radius, opsim_metadata):

    """ Query catsim and make a catalog """

    from lsst.sims.catalogs.generation.db import DBObject, ObservationMetaData

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


def catsim_query_stack10 (objid, constraint, catalog, radius, opsim_metadata):
    
    """ Query catsim and make a catalog """

    from lsst.sims.catalogs.generation.db import CatalogDBObject, ObservationMetaData
    
    obs_metadata = ObservationMetaData(boundType='circle',unrefractedRA=opsim_metadata[1]*180/pi, 
                unrefractedDec=opsim_metadata[2]*180/pi, 
                boundLength=radius,
            mjd=opsim_metadata[5])
    dbobj = CatalogDBObject.from_objid(objid)
#    dbobj.show_db_columns()    
    t = dbobj.getCatalog(catalog, 
            obs_metadata=obs_metadata, 
            constraint=constraint)
#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return t, obs_metadata
