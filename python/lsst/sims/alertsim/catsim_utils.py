""" Query catsim """

def catsim_query(stack_version, **kwargs):

    """ Pass arguments to a function which handles 
    specifics of the stack version """

    if stack_version < 10:
        return catsim_query_stack8(**kwargs)
    else:
        return catsim_query_stack10(**kwargs)


def catsim_query_stack8(objid, constraint, obs_metadata, dia):

    """ Query catsim and make a catalog for stack 8
     
    @param [in] objid of the catsim table
    
    @param [in] constraint is sql constraint for the catsim table
    
    @param [in] obs_metadata is the metadata for the visit

    @param [in] dia is boolean which determines the catalog class 
    i.e if full diasource will be emitted
    """

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
    
    """ Query catsim and make a catalog for stack 10+ 
     
    @param [in] objid of the catsim table
    
    @param [in] constraint is sql constraint for the catsim table
    
    @param [in] obs_metadata is the metadata for the visit

    @param [in] dia is boolean which determines the catalog class 
    i.e if full diasource will be emitted

    """

    from lsst.sims.catalogs.db import CatalogDBObject

    dbobj = CatalogDBObject.from_objid(objid)
    if dia:
        catalog = 'variable_stars_dia'
    else: catalog = 'variable_stars'

    obs_data = dbobj.getCatalog(catalog, 
            obs_metadata=obs_metadata, constraint=constraint)
            #column_outputs=VariableStars.get_column_outputs(obs_metadata.bandpass)) 

#    dbobj.show_db_columns()    
#    dbobj.show_mapped_columns()
#    filename = 'test_reference.dat'
#    t.write_catalog(filename, chunk_size=10)
    return obs_data
