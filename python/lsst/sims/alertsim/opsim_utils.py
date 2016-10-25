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

    raise RuntimeError("How did you get this far?")
    obs_all = []
    
    #query fields for the current night
    night_obs_query = _query_opsim(table, constraint)

    for obs in night_obs_query:
        field_obs = []

        _append_to_file(str(obs[6])+" "+str(obs[1])+"\n")
        
        #constraint for previous observations for the field
        constraint = "expMJD < %s and fieldID = %s" % (obs[6], obs[1])

        #append current night observation transformed 
        #to ObservationMetaData object
        field_obs.append(_array_to_metadata_object(obs, radius))
        
        #query opsim for historical observations, 
        #reversely sorted by mjd
        field_obs_hist_query = sorted(_query_opsim(table, constraint),
                key=itemgetter(6), reverse=True)

        for hist_obs in field_obs_hist_query:
            #append current night observation transformed 
            #to ObservationMetaData object
            field_obs.append(_array_to_metadata_object(hist_obs, radius))
        
        _append_to_file("\n"+str(len(field_obs)))
        #append list (consisting of current and all previous 
        #observations for a field) to a list of all observations
        obs_all.append(field_obs)
        _append_to_file("-----\n")

    return obs_all

def _append_to_file(text):
    """ opens a file and appends text """
    with open("opsim_stats.txt", "a") as myfile:
        myfile.write(text)

def _query_opsim(table, constraint):

    """ A function for opsim query 
    
    @param [in] table is lsst.sims.maf.db.Table object with connection 
    parameters already set

    @param [in] constraint is sql opsim query constraint

    @param [out] result is a list of tuples returned by the query
    """

    result = table.query_columns_Array(colnames=['fieldID',
        'fieldRA', 'fieldDec', 'rawSeeing', 'filter', 'expMJD',
        'fiveSigmaDepth', 'night'], constraint=constraint)

    """ differences between local and remote db column names """
    #result = table.query_columns_Array(colnames=['fieldid',
    #    'fieldra', 'fielddec', 'rawseeing', 'filter', 'expmjd',
    #    'm5sigma', 'night'], constraint=constraint)
    return result

def _array_to_metadata_object(arr, radius):

    """ Turns an array of opsim metadata to ObservationMetaData object

    @param [in] arr is opsim metadata for a single visit

    @param [in] radius is FOV radius

    @param [out] metadata_object is an ObservationMetaData object
    """

    metadata_object = ObservationMetaData(boundType='circle',
                pointingRA=arr[2]*180/pi,
                pointingDec=arr[3]*180/pi,
                boundLength=radius, mjd=arr[6],
                bandpassName=arr[5], m5=arr[7],
                seeing=arr[4])
    return metadata_object
