""" Query opsim """

from lsst.sims.catUtils.baseCatalogModels import *


def opsim_query(objid, constraint):

    dbobj = DBObject.from_objid(objid)
    query = dbobj.query_columns(
            colnames=['Unrefracted_RA','Unrefracted_Dec','Opsim_rawseeing',
                'Opsim_filter', 'Opsim_expmjd'],
            constraint=constraint )
    result = query.exec_query.fetchall()

    print result
    return result

def opsim_query_stack10 (dbadr, constraint):
    import lsst.sims.maf.db as db
    from lsst.sims.catalogs.generation.db import  *



    dbobj=DBObject(dbadr)
    tableid = 'output_opsim3_61'

    table=db.Table(tableid,'obshistid', dbadr)

    ccc=table.query_columns_Array(colnames=['fieldra','fielddec','rawseeing',
                'filter', 'expmjd'],constraint=constraint )


    print ccc
    return ccc
