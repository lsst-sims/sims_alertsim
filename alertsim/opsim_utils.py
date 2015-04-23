""" Query opsim """

from lsst.sims.catUtils.baseCatalogModels import *
import lsst.sims.maf.db as db

DBADDR = "mssql+pymssql://LSST-2:L$$TUser@fatboy.npl.washington.edu:1433/LSST"

def opsim_query(stack_version, **kwargs):
    if stack_version < 10:
        return opsim_query_stack8(**kwargs)
    else:
        return opsim_query_stack10(**kwargs)

def opsim_query_stack8(objid, constraint):

    dbobj = DBObject.from_objid(objid)
    query = dbobj.query_columns(
            colnames=['Unrefracted_RA','Unrefracted_Dec','Opsim_rawseeing',
                'Opsim_filter', 'Opsim_expmjd'],
            constraint=constraint )
    result = query.exec_query.fetchall()

    print result
    return result

def opsim_query_stack10 (objid, constraint):

    table=db.Table(objid,'obshistid', DBADDR)

    result = table.query_columns_Array(colnames=['fieldra','fielddec','rawseeing',
                'filter', 'expmjd'],constraint=constraint )

    print result
    return result
