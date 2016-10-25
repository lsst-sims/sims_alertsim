""" Query opsim """

#from lsst.sims.catUtils.baseCatalogModels import *
from math import pi
from operator import itemgetter, attrgetter
from lsst.sims.utils import ObservationMetaData
from lsst.sims.catUtils.utils import ObservationMetaDataGenerator

def opsim_query(stack_version, **kwargs):

    """ Pass arguments to a function which handles 
        specifics of the stack version """

    if stack_version < 10:
        return opsim_query_stack8(**kwargs)
    else:
        return opsim_query_stack10(**kwargs)

def opsim_query_stack8(opsim_path, objid, radius, constraint):

    """ Query opsim and make a catalog for stack 8
    Obsolete at the moment

    @param [in] opsim_path is the path of the local db

    @param [in] objid of the opsim table

    @param [in] radius is the radius of the field of view for a visit

    @param [in] constraint is sql constraint for the opsim table
    """


    from lsst.sims.catalogs.generation.db import DBObject

    dbobj = DBObject.from_objid(objid)
    query = dbobj.query_columns(
            colnames=['Unrefracted_RA','Unrefracted_Dec','Opsim_rawseeing',
                'Opsim_filter', 'Opsim_expmjd'],
            constraint=constraint )
    result = query.exec_query.fetchall()

    print result
    return result

def opsim_query_stack10 (opsim_path, objid, radius, constraint):

    """ Query opsim and make a catalog for stack 10

    @param [in] opsim_path is the path of the local db

    @param [in] objid of the opsim table

    @param [in] radius is the radius of the field of view for a visit

    @param [in] constraint is sql constraint for the opsim table

    Returns a list of ObservationMetaData
    """

    import lsst.sims.maf.db as db

    if not opsim_path:
        """ access to fatboy """
        raise NotImplementedError("Not yet sure how to do the OpSim queries from fatboy")
        table = db.Table(tableName=objid, idColKey='obshistid', database='LSSTCATSIM', 
                driver='mssql+pymssql', host='localhost', port='51433' )
    else:
        """ local access """
        dbaddress = opsim_path
        obs_gen = ObservationMetaDataGenerator(database=opsim_path, driver='sqlite')
        return obs_gen.getObservationMetaDataFromConstraint(constraint)
