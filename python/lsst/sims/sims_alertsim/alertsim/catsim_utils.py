""" Query catsim """

from math import pi
#from lsst.sims.catUtils.baseCatalogModels import *

def catsimQuery(stack_version, **kwargs):
    """ Determine stack version """

    if stack_version < 10:
        return catsimQueryStack8(**kwargs)
    else:
        return catsimQueryStack10(**kwargs)


def catsimQueryStack8(objid, constraint, catalog, radius, opsim_metadata):
    """ Query catsim and make a catalog """

    from lsst.sims.catalogs.generation.db import DBObject, ObservationMetaData

    obs_metadata = ObservationMetaData(circ_bounds=dict
            (ra=opsim_metadata[1]*180/pi, 
                dec=opsim_metadata[2]*180/pi, 
                radius=radius),
            mjd=opsim_metadata[5])
    dbobj = DBObject.from_objid(objid)
    
    obs_data = dbobj.getCatalog(catalog, 
            obs_metadata=obs_metadata, 
            constraint=constraint)
#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return obs_data, obs_metadata


def catsimQueryStack10 (objid, constraint, catalog, radius, opsim_metadata):
    """ Query catsim and make a catalog 
    
    Parameters
    ----------
    objid : str
        name of Catsim table, e.g. "allstars"
    constraint : str
        constraint for catsim query, e.g. "rmag between 20 and 23.5"
    catalog : str
        name of catsim catalog, choices=["variable_stars", "vanilla_stars", "DIA_sources", "DIA_objects"]
    radius : float
        cone search radius, e.g. 0.05
    opsim_metadata : numpy.record
        record containing observation data (obshistid, field ra, field dec, radius, filter, mjd)
    
    Returns
    -------
    obs_data : 
        Data of observed object. Contains ra, dec and other data, depending of catalog type,
        defined in catalogExamples. e.g. VariableStars object
    obs_metadata : ObservationMetaData object
        Data describing observation (filter, mjd, ...)
    """
    
    from lsst.sims.catalogs.generation.db import CatalogDBObject
    from lsst.sims.utils import ObservationMetaData
    
    obs_metadata = ObservationMetaData(boundType='circle', 
            pointingRA=opsim_metadata[1]*180/pi, 
            pointingDec=opsim_metadata[2]*180/pi, 
            boundLength=radius, mjd=opsim_metadata[5], 
            bandpassName=opsim_metadata[4])
    dbobj = CatalogDBObject.from_objid(objid)
    #dbobj.show_db_columns()    
    obs_data = dbobj.getCatalog(catalog, 
            obs_metadata=obs_metadata, 
            constraint=constraint)
#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return obs_data, obs_metadata
