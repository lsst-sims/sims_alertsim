""" Query opsim """

#from lsst.sims.catUtils.baseCatalogModels import *
from math import pi
from operator import itemgetter, attrgetter
from lsst.sims.utils import ObservationMetaData

def opsim_query(stack_version, **kwargs):
    """ for different stack versions """
    if stack_version < 10:
        return opsim_query_stack8(**kwargs)
    else:
        return opsim_query_stack10(**kwargs)

def opsim_query_stack8(path, objid, radius, constraint):
    """ for stack 8. obsolete at the moment """
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
    """ for stack 10+ """
    import lsst.sims.maf.db as db

    if not opsim_path:
        """ access to fatboy """
        table = db.Table(tableName=objid, idColKey='obshistid', database='LSSTCATSIM', 
                driver='mssql+pymssql', host='localhost', port='51433' )
    else:
        """ local access """
        dbaddress = opsim_path
        table = db.Table('Summary', 'obsHistID', dbaddress)

    obs_all = []
    night_obs_query = _query_opsim(table, constraint)

    for arr in night_obs_query:
        field_obs = []

        _append_to_file(str(arr[6])+" "+str(arr[1])+"\n")
        constraint = "expMJD < %s and fieldID = %s" % (arr[6], arr[1])

        field_obs.append(_array_to_metadata_object(arr, radius))
        field_obs_hist_query = sorted(_query_opsim(table, constraint),
                key=itemgetter(6), reverse=True)

        for arr in field_obs_hist_query:
            field_obs.append(_array_to_metadata_object(arr, radius))
        _append_to_file("\n"+str(len(field_obs)))
        obs_all.append(field_obs)
        _append_to_file("-----\n")

    return obs_all

def _append_to_file(text):
    with open("opsim_stats.txt", "a") as myfile:
        myfile.write(text)

def _query_opsim(table, constraint):

    """ opsim query """
    result = table.query_columns_Array(colnames=['fieldID',
        'fieldRA', 'fieldDec', 'rawSeeing', 'filter', 'expMJD',
        'fiveSigmaDepth', 'night'], constraint=constraint)

    """ differences between local and remote db column names """
    #result = table.query_columns_Array(colnames=['fieldid',
    #    'fieldra', 'fielddec', 'rawseeing', 'filter', 'expmjd',
    #    'm5sigma', 'night'], constraint=constraint)
    return result

def _array_to_metadata_object(arr, radius):
    metadata_object = ObservationMetaData(boundType='circle',
                pointingRA=arr[2]*180/pi,
                pointingDec=arr[3]*180/pi,
                boundLength=radius, mjd=arr[6],
                bandpassName=arr[5], m5=arr[7],
                seeing=arr[4])
    return metadata_object
