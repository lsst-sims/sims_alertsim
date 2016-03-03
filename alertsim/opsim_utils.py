""" Query opsim """

#from lsst.sims.catUtils.baseCatalogModels import *

def opsim_query(stack_version, **kwargs):
    """ for different stack versions """
    if stack_version < 10:
        return opsim_query_stack8(**kwargs)
    else:
        return opsim_query_stack10(**kwargs)

def opsim_query_stack8(objid, constraint):
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

def opsim_query_stack10 (objid, constraint):
    """ for stack 10+ """
    import lsst.sims.maf.db as db
    #from lsst.sims.catalogs.generation.db import CatalogDBObject 

    #dbobj = CatalogDBObject.from_objid(objid)
    table = db.Table(tableName=objid, idColKey='obshistid', database='LSSTCATSIM', 
            driver='mssql+pymssql', host='localhost', port='51433' )

    result = table.query_columns_Array(colnames=['fieldra', 'fielddec', 
            'rawseeing', 'filter', 'expmjd'],constraint=constraint )

    print result
    return result
