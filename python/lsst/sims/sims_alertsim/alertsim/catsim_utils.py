""" Query catsim """

def catsim_query(stack_version, **kwargs):

    """ Determine stack version """

    if stack_version < 10:
        return catsim_query_stack8(**kwargs)
    else:
        return catsim_query_stack10(**kwargs)


def catsim_query_stack8(objid, constraint, obs_metadata):

    """ Query catsim and make a catalog """

    from lsst.sims.catalogs.generation.db import DBObject

    dbobj = DBObject.from_objid(objid)
    
    obs_data = dbobj.getCatalog('variable_stars', 
            obs_metadata=obs_metadata, 
            constraint=constraint)

#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return obs_data


def catsim_query_stack10 (objid, constraint, obs_metadata):
    
    """ Query catsim and make a catalog """

    from lsst.sims.catalogs.generation.db import CatalogDBObject
    from lsst.sims.sims_alertsim.catalogs import *
    
    dbobj = CatalogDBObject.from_objid(objid)
    #dbobj.show_db_columns()    

    obs_data = dbobj.getCatalog('variable_stars', 
            obs_metadata=obs_metadata, constraint=constraint)
            #column_outputs=VariableStars.get_column_outputs(obs_metadata.bandpass)) 

#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return obs_data
