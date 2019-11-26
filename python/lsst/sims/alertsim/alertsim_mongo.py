""" Main module for mongodb generation """
from __future__ import print_function
from __future__ import absolute_import

from copy import deepcopy
import numpy as np
from timeit import default_timer as timer
from builtins import zip
import os
import sys
import time
import functools
import gc
from pymongo import MongoClient

from lsst.sims.alertsim import catsim_utils, opsim_utils
from lsst.sims.alertsim.catalogs import dia_transformations as dia_trans
from lsst.sims.catUtils.mixins import ParametrizedLightCurveMixin
from lsst.sims.photUtils import cache_LSST_seds
from lsst.sims.catUtils.utils import FastStellarLightCurveGenerator

BANDNAMES = ['u', 'g', 'r', 'i', 'z', 'y']
STACK_VERSION = 10
CATSIM_CONSTRAINT = "varParamStr not like 'None'"

def main(opsim_table=None, catsim_table='epycStarBase',
         opsim_night=None, opsim_filter=None, opsim_mjd = None,
         opsim_path=None, catsim_constraint = CATSIM_CONSTRAINT,
         radius=1.75, history=True,
         dia=True, token=None):


    """ Controls all of Alertsim functionalities
        
    Takes input args from cmd line parser (examples/exampleParserMongo.py) 
    or other script, queries opsim & catsim, generates json events 
    and stores them into mongodb.

    @param [in] opsim_table is objid of opsim table to be queried on fatboy
    
    @param [in] catsim_table is objid of catsim table to be queried on fatboy
   
    @param [in] opsim_night is constraint for opsim query 
    
    @param [in] opsim_filter is constraint for opsim query. If none, it
    will return observations through all filters
    
    @param [in] opsim_mjd is constraint for opsim query 

    @param [in] opsim_path is path of local opsim DB. If left empty, 
    fatboy is queried
    
    @param [in] catsim_constraint is sql (string) constraint for catsim query

    @param [in] radius is radius of catsim query

    @param [in] history is boolean which determines whether historical 
    occurancies of same DIASource are emitted within each VOEvent

    @param [in] dia is boolean which switches between vanilla attributes
    and full DIASource attributes for each VOEvent

    """

    mongo_client = MongoClient('localhost', 27017)

    """ THIS IS A SKETCH OF TOKEN FUNCTIONALITY """
    if token is not None:
        dbnames = mongo_client.list_database_names()
        if token not in dbnames:
            print("A database related with this token doesn't exist.\n"
                    "Please insert a correct token or start the script\n"
                    "without a token to create a new database")
            exit(0)
        else:
            print("Working with the existing db %s" % (token))
            db_name = str(token)
            pass
    else:
        token = int(time.time())
        print("Creating new token %s. If the program or connection breaks,\n"
                "you can continue from the point it broke by entering the --token argument" % (token))
        db_name = str(token)
    
    db = mongo_client[db_name]
    alerts_mongo_collection = db['alerts']
    metadata_mongo_collection = db['metadata']
    
    metadata_dict = {"token":token, "last_obsHistID":None, "objIds":[]}
    metadata_mongo_collection.insert_one(metadata_dict)

    print("fetching opsim results...")


    """ matrix of all observations per field up to current mjd REVERSED """
    obs_matrix = opsim_utils.opsim_query(stack_version=STACK_VERSION, 
            opsim_path=opsim_path, objid=opsim_table, radius=radius, 
            opsim_night=opsim_night, opsim_filter=opsim_filter, 
            opsim_mjd=opsim_mjd, history=history, reverse=True)

    print("opsim result fetched (in reverse order) and transformed to ObservationMetaData objects")

    """ slice the matrix from the last stored obsHistID """
    last_obsHistID = metadata_dict["last_obsHistID"]
    if last_obsHistID is not None:
        obs_matrix[:] = [x for x in obs_matrix if x[0].OpsimMetaData['obsHistID']<last_obsHistID]

    plc = ParametrizedLightCurveMixin()
    plc.load_parametrized_light_curves()
    
    if history:
        cache_LSST_seds()

    """ a set of id's of diaObjects which were previously serialized """
    already_issued = set()

    for obs_per_field in obs_matrix:

        """ current observation - largest mjd from a sorted list  """
        obs_metadata = obs_per_field[0]

        """
        make an additional CatSim constraint based on fiveSigmaDepth value
        from OpsimMetaData
        """
        full_constraint = catsim_constraint + _get_additional_constraint(obs_metadata)
        print('### full constraint: %s' % (full_constraint))
        
        obs_data = catsim_utils.catsim_query(stack_version=STACK_VERSION,
                objid=catsim_table, constraint=full_constraint,
                obs_metadata=obs_metadata, dia=dia)

        """ query catsim, pack voevents and send/serialize """
        query_and_dispatch(obs_data, obs_metadata, obs_per_field, history, 
                radius, opsim_path, full_constraint, 
                already_issued, alerts_mongo_collection)

    mongo_client.close()


def query_and_dispatch(obs_data, obs_metadata, observations_field, 
                       history, radius, opsim_path, 
                       full_constraint, already_issued, alerts_mongo_collection):

    """ Iterate over catalog and either:
        a) serialize data as JSON, divided into files by CCD number
        b) send data as VOEvents to a remote machine

    @param [in] obs_data is an instantiation of InstanceCatalog

    @param [in] obs_metadata is the metadata for the given night, 
    or observation_field[0], kept for clarity

    @param [in] observations_field is a list of all observations 
    for the given field

    @param [in] history is boolean which determines whether historical 
    occurancies of same DIASource are emitted within each VOEvent
    
    """

    """ a list of alert dicts for a visit that will eventually be serialized """
    list_of_alert_dicts = []
    catsim_chunk_size = 3000

    if not history:
        for line in obs_data.iter_catalog(chunk_size=catsim_chunk_size):

            diaSource_dict = dict(zip(obs_data.iter_column_names(), line))
            
            # convert numpy types to scalar
            # JSON can't serialize numpy
            _numpy_to_scalar(diaSource_dict)

            alert_dict = {'alertId':diaSource_dict['diaSourceId'], 
                    'diaSource':diaSource_dict, 
                    'prvDiaSources':[]}

            list_of_alert_dicts.append(alert_dict)
    
    else:
        lc_gen = FastStellarLightCurveGenerator(obs_data.db_obj, opsim_path)
        
        print("#### radius = %f" % (radius))
        ra1=obs_metadata.pointingRA - radius/np.cos(np.radians(obs_metadata.pointingDec))
        ra2=obs_metadata.pointingRA + radius/np.cos(np.radians(obs_metadata.pointingDec))
        dec1=obs_metadata.pointingDec - radius
        dec2=obs_metadata.pointingDec + radius

        print("ra %f - %f, decl %f - %f" % (ra1, ra2, dec1, dec2))
        pointings = lc_gen.get_pointings((ra1, ra2), (dec1, dec2), expMJD=(obs_metadata.mjd.TAI-365, obs_metadata.mjd.TAI), boundLength=radius)
        
        print("number of pointings %d: " % sum(len(x) for x in pointings))
        lc_dict, truth_dict = lc_gen.light_curves_from_pointings(pointings=pointings, constraint=full_constraint, chunk_size=1000)

        print("done with lc's")
        print("%d observations of this field for previous 365 days" %len(observations_field))

        catsim_timer = timer()
        counter = 0
        first_time = True
        
        for line in obs_data.iter_catalog(chunk_size=catsim_chunk_size):
            
            if (not first_time and counter==0): 
                print("Retrieve new chunk of events %s s" % (timer()-catsim_timer))
            
            first_time = False

            counter = counter + 1
            if (counter % 100 == 0):
                print("%s %s" % (counter, timer()))
            
            diaSource_dict = dict(zip(obs_data.iter_column_names(), line))

            diaObjectId = diaSource_dict['diaObjectId']
            
            if diaObjectId not in already_issued:

                already_issued.add(diaObjectId)

                # convert numpy types to scalar
                # JSON can't serialize numpy
                _numpy_to_scalar(diaSource_dict)

                """faking this for now due to int64 problems"""
                #diaSource_dict['diaSourceId'] = int(dia_trans.diaSourceId(int(np.asscalar(obs_metadata.OpsimMetaData['obsHistID'])), 
                #        diaObjectId))

                lc = lc_dict[diaObjectId]

                diaSource_history = []
                
                for filterName, nestedDict in lc.items():
                    for i, mjd in enumerate(nestedDict['mjd']):
                    
                        # find a proper ObservationMetaData object by mjd.
                        # this should be ok if opsim/lc data is consistent, 
                        # however it would be healthier if some smart exception
                        # is added
                        current_metadata = next((x for x in observations_field if x.mjd.TAI == mjd), None)

                        # copy diaSource values and adjust filter, mjd, mag, error
                        temp_dict = deepcopy(diaSource_dict)

                        totMag = nestedDict['mag'][i]
                        meanMag = temp_dict['lsst_%s' % filterName]-temp_dict['delta_lsst_%s' % filterName]
                    
                        totFlux = dia_trans.fluxFromMag(totMag)
                        meanFlux = dia_trans.fluxFromMag(meanMag)
                        diaFlux = totFlux - meanFlux

                        # error is not handled yet!!
                        error = nestedDict['error'][i]

                        obsHistID = int(np.asscalar(current_metadata.OpsimMetaData['obsHistID']))

                        # apply transformations to form diaSource attributes
                        temp_dict['filterName'] = filterName
                        #temp_dict['lsst_%s' % filterName] = totMag
                        #temp_dict['delta_lsst_%s' % filterName] = totMag - meanMag
                        temp_dict['midPointTai'] = dia_trans.midPointTai(mjd)
                        temp_dict['ccdVisitId'] = dia_trans.ccdVisitId(obsHistID, 
                                temp_dict['ccdVisitId']//10000)
                        #temp_dict['diaSourceId'] = int(dia_trans.diaSourceId(obsHistID,
                        #    diaObjectId))
                        temp_dict['apFlux'] = diaFlux
                        # Append to the list of historical instances
                        diaSource_history.append(temp_dict)
                    
                        # Convert newly calculated values from numpy to scalar
                        _numpy_to_scalar(temp_dict)
                    
                for dic in diaSource_history + [diaSource_dict]:
                    list_of_keys = list(dic.keys())
                    for k in list_of_keys:
                        if k.startswith('lsst_') or k.startswith('delta_lsst_'):
                            dic.pop(k)
                
                alert_dict = {'alertId':diaSource_dict['diaSourceId'], 
                        'diaSource':diaSource_dict, 
                        'prvDiaSources':diaSource_history}

                list_of_alert_dicts.append(alert_dict)
                
                
                if (counter==catsim_chunk_size):
                    print('ready to write %d events to mongodb' % catsim_chunk_size)

                    mongo_write_timer = timer()
                    alerts_mongo_collection.insert_many(list_of_alert_dicts)
                    print('events written to mongodb in %s s' % (timer() - mongo_write_timer))

                    list_of_alert_dicts=[]
                    counter = 0
                    gc.collect()
                    del gc.garbage[:]

    """ deal with the rest of events """
    print('ready to write %d events to mongodb' % len(list_of_alert_dicts))
    mongo_write_timer = timer()
    alerts_mongo_collection.insert_many(list_of_alert_dicts)
    print('events written to mongodb in %s s' % (timer() - mongo_write_timer))
    print(sys.getsizeof(already_issued))
    print(len(gc.garbage[:]))
    gc.collect()
    print(len(gc.garbage[:]))
    del gc.garbage[:]

def _remove_band_attrs(obj, bandname):
    """ Remove attributes not connected to the given bandname
    
    @param [in] obj is the object with astronomical data and metadata

    @param [in] bandname is the bandname for the visit
    
    """


    # this may not be the safest way and needs to be revised
    for key in list(obj.__dict__.keys()):
        if ('lsst' in key) and not (key.endswith(bandname)):
            obj.__dict__.pop(key)

"""
def _rename_band_attr(obj, bandname):
        for key in obj.__dict__:
            if 'lsst' in key:
                new_key = key[:-1] + bandname
                obj.__dict__[new_key] = obj.__dict__.pop(old_name)
"""

def _rsetattr(obj, attr, val):
    """ fix setattr lack of dot notation support """
    pre, _, post = attr.rpartition('.')
    return setattr(functools.reduce(getattr,
        [obj]+pre.split('.')) if pre else obj, post, val)

def _get_additional_constraint(obs_metadata):
    """ make Catsim constraint out of Opsim metadata parameters """
    fiveSigmaDepth = obs_metadata.OpsimMetaData['fiveSigmaDepth']
    opsim_filter = obs_metadata.OpsimMetaData['filter']
    new_constraint = " and %smag <= %f" % (opsim_filter, fiveSigmaDepth)
    return new_constraint

def _numpy_to_scalar(d):

    """ Recursively change all numpy types to scalar

    @param[in] d is a dictionary containing single alert

    """
    for k, v in d.items():
        if isinstance(d[k], dict):
            _numpy_to_scalar(d[k])
        elif isinstance(d[k], np.generic):
            d[k] = np.asscalar(d[k])
        else:
            pass
