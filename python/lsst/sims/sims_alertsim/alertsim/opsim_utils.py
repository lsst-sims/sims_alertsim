""" Query opsim """

#from lsst.sims.catUtils.baseCatalogModels import *

def opsimQuery(stack_version, **kwargs):
    """ for different stack versions """
    if stack_version < 10:
        return opsimQueryStack8(**kwargs)
    else:
        return opsimQueryStack10(**kwargs)

def opsimQueryStack8(objid, constraint):
    """ for stack 8 """
    from lsst.sims.catalogs.generation.db import DBObject

    dbobj = DBObject.from_objid(objid)
    query = dbobj.query_columns(
            colnames=['Unrefracted_RA','Unrefracted_Dec','Opsim_rawseeing',
                'Opsim_filter', 'Opsim_expmjd'],
            constraint=constraint )
    result = query.exec_query.fetchall()

    print result
    return result

def opsimQueryStack10 (objid, constraint):
    """ for stack 10+ 
    
    Parameters
    ----------
    objid : str
        opsim objid, e.g. "output_opsim3_61"
    constraint : str
        constraint for opsim query, e.g. (night=10 and rawseeing<0.6) and filter like 'i'
    
    Returns
    -------
    result : numpy.ndarray
        set of observations satisfying given query
        Each observation contains (obshistid, fieldra, fielddec, rawseeing, filter, expmjd).
    """
    
    import lsst.sims.maf.db as db
    #from lsst.sims.catalogs.generation.db import CatalogDBObject 

    #dbobj = CatalogDBObject.from_objid(objid)
    table = db.Table(tableName=objid, idColKey='obshistid', database='LSSTCATSIM', 
            driver='mssql+pymssql', host='localhost', port='51433' )

    result = table.query_columns_Array(colnames=['fieldra', 'fielddec', 
            'rawseeing', 'filter', 'expmjd'],constraint=constraint )

    print result
    return result
