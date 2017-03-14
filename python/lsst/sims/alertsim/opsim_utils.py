""" Query opsim """
from __future__ import print_function

#from lsst.sims.catUtils.baseCatalogModels import *
import numpy as np
from lsst.sims.utils import ObservationMetaData
from lsst.sims.catUtils.utils import ObservationMetaDataGenerator

def opsim_query(stack_version, **kwargs):

    """ Pass arguments to a function which handles 
        specifics of the stack version """

    if stack_version < 10:
        return opsim_query_stack8(**kwargs)
    else:
        return opsim_query_stack10(**kwargs)

def opsim_query_stack8(opsim_path, objid, radius, opsim_night, 
        opsim_filter, opsim_mjd, history):

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

    print(result)
    return result

def opsim_query_stack10(opsim_path, objid, radius, opsim_night, 
        opsim_filter, opsim_mjd, history):

    """ Query opsim and make a catalog for stack 10

    @param [in] opsim_path is the path of the local db

    @param [in] objid of the opsim table

    @param [in] radius is the radius of the field of view for a visit

    @param [in] constraint is sql constraint for the opsim table

    Returns a list of ObservationMetaData
    """

    import lsst.sims.catalogs.db as db

    if not opsim_path:
        """ access to fatboy """
        raise NotImplementedError("Not yet sure how to do the OpSim queries from fatboy")
        table = db.CatalogDBObject(table=objid, idColKey='obshistid', database='LSSTCATSIM',
                driver='mssql+pymssql', host='localhost', port='51433' )
    else:
        """ local access """
        dbaddress = opsim_path
        obs_gen = ObservationMetaDataGenerator(database=opsim_path, driver='sqlite')
        #return obs_gen.getObservationMetaDataFromConstraint(constraint)
        obs_all = obs_gen.getObservationMetaData(night=opsim_night, 
                    telescopeFilter=opsim_filter, expMJD=opsim_mjd)
        
        obs_history = []

        if history:
            obs_history = _convert_obs_to_history(obs_all)
        else:
            # we do not need the historical information; construct a dummy history
            mjd_arr = np.array([obs.mjd.TAI for obs in obs_all])
            obs_history = np.array(obs_all)[np.argsort(mjd_arr)]
            obs_history = [[obs, None] for obs in obs_history]

        return obs_history

def _convert_obs_to_history(obs_list):
    """
    Take a list of ObservationMetaData and rearrange it into a 2-d list in which each row
    corresponds to the current ObservationMetaData but also contains all of the prior
    observations of the same field up to that date in sorted order
    """
    # sort the ObservationMetaData in chronological order
    mjd_array = np.array([obs.mjd.TAI for obs in obs_list])
    sorted_dex = np.argsort(mjd_array)
    if not isinstance(obs_list, np.ndarray):
        obs_list = np.array(obs_list)

    obs_list = obs_list[sorted_dex]

    field_arr = np.array([obs.OpsimMetaData['fieldID'] for obs in obs_list])

    output_history = []
    for ix, obs in enumerate(obs_list):
        # find all of the other observations of the same field
        other_obs = np.where(field_arr[:ix] == obs.OpsimMetaData['fieldID'])[0]
        current_obs = [obs] + [obs_list[other_obs[ix]] for ix in range(len(other_obs)-1,-1,-1)]
        output_history.append(current_obs)

    return output_history
