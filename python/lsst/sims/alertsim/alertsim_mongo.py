""" Main module for mongodb generation """
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
import time
import functools
import gc
import numpy as np
from timeit import default_timer as timer
from copy import deepcopy
from builtins import zip
try:
    from pymongo import MongoClient
    _mongo_installed = True
except:
    _mongo_installed = False

from lsst.sims.alertsim import catsim_utils, opsim_utils, avro_utils
from lsst.sims.alertsim.catalogs import dia_transformations as dia_trans
from lsst.sims.alertsim.other import Spinner
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

    @param [in] token is a unique identifier of an alertsim run. Can be
    used to continue previous, broken run. It is also the name of the Mongo
    database for that run.
    """
    global _mongo_installed
    if not _mongo_installed:
        _raise_no_mongo("main")

    mongo_client = MongoClient('localhost', 27017)

    """ A token is used to continue an alertsim run from the point it broke. 
    As alertsim is time and memory intensive, with an online tunnel required
    for querying catsim, it can break easily. This assures seamless continuation."""

    if token is not None:
        dbnames = mongo_client.list_database_names()
        if str(token) not in dbnames:
            print("(alertsim) A database related with this token doesn't exist. "
                    "Please insert a correct token or start the script without "
                    "a token to create a new database.")
            exit(0)
        else:
            print("(alertsim) Continuing an existing alertsim run.")
            print("(alertsim) Working with the database %s." % (token))
            db_name = str(token)
            pass
    else:
        token = int(time.time())
        print("(alertsim) Creating new token %s. If the program or "
                "connection breaks, you can continue from the point "
                "it broke by entering the --token argument." % (token))
        db_name = str(token)
    
    db = mongo_client[db_name]
    alerts_mongo_collection = db['alerts']
    metadata_mongo_collection = db['metadata']

    metadata_dict = metadata_mongo_collection.find_one()
    
    if metadata_dict is None:
        metadata_dict = {"token":token, "last_obsHistID":None, 
                "fieldIDs":[]}
        metadata_mongo_collection.insert_one(metadata_dict)
    else:
        print("(alertsim) Last obsHistID for which data was serialized "
                "was %s" % (metadata_dict['last_obsHistID']))

    with Spinner(message="(alertsim) Fetching opsim results "):
        """ matrix of all observations per field up to current mjd REVERSED """
        obs_matrix = opsim_utils.opsim_query(stack_version=STACK_VERSION, 
                opsim_path=opsim_path, objid=opsim_table, radius=radius, 
                opsim_night=opsim_night, opsim_filter=opsim_filter, 
                opsim_mjd=opsim_mjd, history=history, reverse=True)
    
    print("(alertsim) Opsim matrix fetched (in reverse order)")

    """ slice the matrix from the last stored obsHistID """
    last_obsHistID = metadata_dict["last_obsHistID"]
    if last_obsHistID is not None:
        obs_matrix[:] = [x for x in obs_matrix if \
                x[0].OpsimMetaData['obsHistID']<last_obsHistID]
    
    """ a set of fieldID's for which catsim and lc data were already
    serialized. This is done in advance to avoid multiple lc calls for 
    same diaObjects (objects from the same field) """
    fieldIDs_to_skip = set(metadata_dict["fieldIDs"])

    plc = ParametrizedLightCurveMixin()
    plc.load_parametrized_light_curves()
    
    if history:
        cache_LSST_seds()

    """ MJD for the beginning of the night. """
    night_mjd = obs_matrix[-1][0].mjd.TAI
    alerts_total_count = 0

    print("(alertsim) MJD at the beginning of this night %s" % (night_mjd))
    
    for obs_per_field in obs_matrix:

        print("(alertsim) ---- new observation ----")

        """ current observation - largest mjd from a sorted list  """
        obs_metadata = obs_per_field[0]
        #from pprint import pprint
        #pprint(vars(obs_metadata))
        current_obsHistID = obs_metadata.OpsimMetaData['obsHistID']
        current_fieldID = obs_metadata.OpsimMetaData['fieldID']

        #import psutil
        #for proc in psutil.process_iter():
        #    print(proc.open_files())

        """ We process the whole data for the field for the night
        once we runt into it (for lc performance sake), so skip when
        you see it next time """
        if current_fieldID in fieldIDs_to_skip:
            print("(alertsim) Field %d was already processed for the entire night. "
                    "Skipping observation %d and continuing to the next one." \
                    % (current_obsHistID, current_fieldID))
        
        else:
            print("(alertsim) Observation %d, field %d" % (current_obsHistID, 
                current_fieldID))
            
            """ make an additional CatSim constraint based on fiveSigmaDepth value
            from OpsimMetaData """
            full_constraint = catsim_constraint + _get_additional_constraint(obs_metadata)
            print('(alertsim) full constraint: %s' % (full_constraint))
        
            obs_data = catsim_utils.catsim_query(stack_version=STACK_VERSION, 
                    objid=catsim_table, constraint=full_constraint, 
                    obs_metadata=obs_metadata, dia=dia)

            """ query catsim and serialize events to mongodb """
            query_and_serialize(obs_data, obs_metadata, obs_per_field, history, 
                    radius, opsim_path, full_constraint, alerts_mongo_collection, night_mjd)

        """ update last IDs and fields to skip 
        THIS SHOULD BE IMPROVED: PART OF THE DATA MAYBE GOT SERIALIZED
        BUT THE PROGRAM BROKE IN THE MIDDLE OF THE QUERY
        SOME FLUSH OPTIONS MAYBE? SEE FSYNC
        THIS IS NOT THE ONLY POINT AS THERE ARE PERFORMANCE AND MEMORY ISSUES
        """
        last_obsHistID = int(obs_metadata.OpsimMetaData['obsHistID'])

        if history: fieldIDs_to_skip.add(int(obs_metadata.OpsimMetaData['fieldID']))
        
        metadata_dict = {"token":token, "last_obsHistID":last_obsHistID, 
                "fieldIDs":fieldIDs_to_skip}
        
        print("(alertsim) updating mongo metadata")
        print(metadata_dict)
        metadata_mongo_collection.update_one({"token":token},
                {"$set": {"last_obsHistID":last_obsHistID, "fieldIDs":list(fieldIDs_to_skip)} })

    mongo_client.close()


def query_and_serialize(obs_data, obs_metadata, observations_field, 
                       history, radius, opsim_path,
                       full_constraint, alerts_mongo_collection, night_mjd):

    """ Iterate over catalog, transform data to dicts according to 
        the avro schema, add history (if turned on) and serialize to mongodb

    @param [in] obs_data is an instantiation of InstanceCatalog

    @param [in] obs_metadata is the metadata for the given night, 
    or observation_field[0], kept for clarity

    @param [in] observations_field is a list of all observations 
    for the given field

    @param [in] history is boolean which determines whether historical 
    occurancies of same DIASource are emitted within each VOEvent
    
    """

    """ a list of alert dicts for a visit that will eventually be serialized """
    global alerts_total_count
    
    list_of_alert_dicts = []
    catsim_chunk_size = 3000

    cutout_file = open("avsc/sample_cutouts/stamp-676.fits.gz", "rb")
    cutout_data = cutout_file.read()
    cutout_difference = cutout_template = {"fileName":"stamp-676", 
            "stampData":cutout_data}

    if not history:
        for line in obs_data.iter_catalog(chunk_size=catsim_chunk_size):

            alerts_total_count += 1
            diaSource_dict = dict(zip(obs_data.iter_column_names(), line))
            
            # convert numpy types to scalar
            # JSON can't serialize numpy
            _numpy_to_scalar(diaSource_dict)

            alert_dict = {'alertId':alerts_total_count,
                    'diaSource':diaSource_dict, 'prvDiaSources':[],
                    'cutoutTemplate':cutout_template,
                    'cutoutDifference':cutout_difference}

            list_of_alert_dicts.append(alert_dict)
    
    else:
        lc_gen = FastStellarLightCurveGenerator(obs_data.db_obj, opsim_path)
        
        #print("(alertsim) radius = %f" % (radius))
        ra1=obs_metadata.pointingRA - \
                radius/np.cos(np.radians(obs_metadata.pointingDec))
        ra2=obs_metadata.pointingRA + \
                radius/np.cos(np.radians(obs_metadata.pointingDec))
        dec1=obs_metadata.pointingDec - radius
        dec2=obs_metadata.pointingDec + radius

        year = 365
        observations_year = len(observations_field)
        if observations_year > 200: catsim_chunk_size = 150
        """
        if observations_year > 200:
            print("(alertsim) %d observations for previous year exceeds " \
                    "limit of 200. This is probably a deep drilling field. " \
                    "Number of days in history will be reduced to meet a " \
                    "criteria of up to 200 historical diaSources per year." \
                    % (observations_year))
            year = (200*365)//observations_year
        """

        #print("(alertsim) ra %f - %f, decl %f - %f" % (ra1, ra2, dec1, dec2))
        """ expMJD range is inclusive, so we are deducting ~20sec in order not
        to duplicate current visit """
        pointings = lc_gen.get_pointings((ra1, ra2), (dec1, dec2), 
                expMJD=(obs_metadata.mjd.TAI-year, obs_metadata.mjd.TAI-0.0002),
                boundLength=radius)

        print("(alertsim) %d observations of this field for previous %d days" \
                % (sum(len(x) for x in pointings), year))

        lc_dict, truth_dict = lc_gen.light_curves_from_pointings(pointings=pointings, 
                constraint=full_constraint, chunk_size=1000)

        print("(alertsim) Done with lc's")

        catsim_timer = timer()
        counter = 0
        first_time = True
        
        for line in obs_data.iter_catalog(chunk_size=catsim_chunk_size):
            
            alerts_total_count += 1

            if (not first_time and counter==0):
                print("(alertsim) Retrieve new chunk of events %s s" % \
                        (timer()-catsim_timer))

            counter = counter + 1
            if (counter % 100 == 0):
                print("(alertsim) %s %s s" % (counter, timer() - catsim_timer))
                catsim_timer = timer()
            
            diaSource_dict = dict(zip(obs_data.iter_column_names(), line))
            diaObjectId = diaSource_dict['diaObjectId']

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
                    current_metadata = next((x for x in observations_field \
                            if x.mjd.TAI == mjd), None)

                    # copy diaSource values and adjust filter, mjd, mag, error
                    temp_dict = deepcopy(diaSource_dict)

                    totMag = nestedDict['mag'][i]
                    meanMag = temp_dict['lsst_%s' % filterName] - \
                            temp_dict['delta_lsst_%s' % filterName]
                
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
                    print(temp_dict['midPointTai'])
                    temp_dict['ccdVisitId'] = dia_trans.ccdVisitId(obsHistID, 
                                temp_dict['ccdVisitId'] % 10000)
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
            
            diaSource_history.sort(key=lambda x : x['midPointTai'], 
                    reverse = True)
            #print(diaSource_dict['midPointTai'])
            #for x in diaSource_history:
            #    print(x['midPointTai'], end=" ")

            while diaSource_dict['midPointTai'] >= night_mjd:

                alerts_total_count += 1

                alert_dict = {'alertId':alerts_total_count, 
                        'diaSource':diaSource_dict,
                        'prvDiaSources':diaSource_history,
                        'cutoutTemplate':cutout_template,
                        'cutoutDifference':cutout_difference}

                if first_time: avro_utils.validate_alert(alert_dict)
                first_time = False

                list_of_alert_dicts.append(alert_dict)
                
                diaSource_dict = diaSource_history[0]
                diaSource_history.pop(0)

            if (counter==catsim_chunk_size):
                _write_to_mongo(alerts_mongo_collection, list_of_alert_dicts)
                
                list_of_alert_dicts=[]
                counter = 0

                gc.collect()
                del gc.garbage[:]

    cutout_file.close()

    """ deal with the rest of events """
    _write_to_mongo(alerts_mongo_collection, list_of_alert_dicts)

    gc.collect()
    del gc.garbage[:]


def _write_to_mongo(collection, list_of_alert_dicts):
    """ Serialize events to mongodb

    @param [in] list_of_alert_dicts is a list of alerts formatted
    according to the valid avro schema
    
    """

    if list_of_alert_dicts:
        print('(alertsim) Ready to write %d events to mongodb' % \
                len(list_of_alert_dicts))
        mongo_write_timer = timer()
        collection.insert_many(list_of_alert_dicts)
        print('(alertsim) Events written to mongodb in %s s' % (timer() - \
                mongo_write_timer))


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

def _raise_no_mongo(method_name):
    msg = "To use %s you must install pymongo from "
    "https://api.mongodb.com/python/current/. You might "
    "use pip install pymongo" % method_name
    raise RuntimeError(msg)
