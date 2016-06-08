""" Query catsim """

def catsim_query(stack_version, **kwargs):

    """ Determine stack version """

    if stack_version < 10:
        return catsim_query_stack8(**kwargs)
    else:
        return catsim_query_stack10(**kwargs)


def catsim_query_stack8(objid, constraint, obs_metadata, dia):

    """ Query catsim and make a catalog """

    from lsst.sims.catalogs.generation.db import DBObject

    dbobj = DBObject.from_objid(objid)
    
    if dia:
        catalog = 'variable_stars_dia'
    else: catalog = 'variable_stars'

    obs_data = dbobj.getCatalog(catalog, 
            obs_metadata=obs_metadata, 
            constraint=constraint)

#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return obs_data


def catsim_query_stack10 (objid, constraint, obs_metadata, dia):
    
    """ Query catsim and make a catalog """

    from lsst.sims.catalogs.generation.db import CatalogDBObject
    from lsst.sims.sims_alertsim.catalogs import *
    
    dbobj_stars = CatalogDBObject.from_objid(objid)
    dbobj_gals = CatalogDBObject.from_objid('galaxyTiled')

    catalog_stars = 'variable_stars'
    catalog_gals = 'variable_galaxies'

    if dia:
        catalog_stars += "_dia"
        catalog_gals += "_dia"

    obs_data = []

    obs_data.append(dbobj_stars.getCatalog(catalog_stars, 
            obs_metadata=obs_metadata, constraint=constraint))
            #column_outputs=VariableStars.get_column_outputs(obs_metadata.bandpass)) 
    obs_data.append(dbobj_gals.getCatalog(catalog_gals, 
            obs_metadata=obs_metadata, constraint='varParamStr not like \'None\''))

    #for a in obs_data:
    #    print vars(a)
#    dbobj.show_db_columns()    
#    dbobj.show_mapped_columns()
#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return obs_data
