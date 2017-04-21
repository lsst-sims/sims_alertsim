""" Main module """
from __future__ import print_function
from __future__ import absolute_import

from builtins import zip
import os
import time
import functools
from . import catsim_utils, opsim_utils, avro_utils
from copy import deepcopy
from lsst.sims.alertsim.dataModel import DataMetadata, CelestialObject
from lsst.sims.alertsim.generateVOEvent import VOEventGenerator
from lsst.sims.alertsim.broadcast import *
from lsst.sims.alertsim.catalogs import *

BANDNAMES = ['u', 'g', 'r', 'i', 'z', 'y']
STACK_VERSION = 10
CATSIM_CONSTRAINT = "varParamStr not like 'None'"
IPADDR = "147.91.240.29"

def main(opsim_table=None, catsim_table='allstars', 
         opsim_night=None, opsim_filter=None, opsim_mjd = None, 
         opsim_path=None, catsim_constraint = CATSIM_CONSTRAINT, 
         radius=1.75, protocol=None, ipaddr=IPADDR, port=8098, 
         header=True, history=True, dia=True, serialize_json=False):


    """ Controls all of Alertsim functionalities
        
    Takes input args from cmd line parser (examples/exampleParser.py) 
    or other script, queries opsim & catsim, generates and broadcasts 
    VOEvents via TCP to a specified ip address or serializes 
    data to json format.

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

    @param [in] protocol is tcpip or multicast

    @param [in] ipaddr is ip address of the VOEvent stream receiver

    @param [in] port is the tcp port of the VOEvent stream receiver

    @param [in] header is boolean which includes/excludes 4 byte hex header in 
    each VOEvent message (VOEvent standard asks for a header)

    @param [in] history is boolean which determines whether historical 
    occurancies of same DIASource are emitted within each VOEvent

    @param [in] dia is boolean which switches between vanilla attributes
    and full DIASource attributes for each VOEvent

    @param [in] serialize_json is boolean. In case of true, events are not 
    emitted but serialized in JSON format, divided into files based on CCD 
    number
    """


    print("fetching opsim results...")


    """ matrix of all observations per field up to current mjd """
    obs_history = opsim_utils.opsim_query(stack_version=STACK_VERSION, 
            opsim_path=opsim_path, objid=opsim_table, radius=radius, 
            opsim_night=opsim_night, opsim_filter=opsim_filter, 
            opsim_mjd=opsim_mjd, history=history)

    print("opsim result fetched and transformed to ObservationMetaData objects")

    if not serialize_json:

        """ establish connection """
        sender = get_sender(protocol, ipaddr, port, header)

        for obs_per_field in obs_history:

            """ current observation - largest mjd from a sorted list  """
            obs_metadata = obs_per_field[0]

            obs_data = catsim_utils.catsim_query(stack_version=STACK_VERSION,
                    objid=catsim_table, constraint=catsim_constraint,
                    obs_metadata=obs_metadata, dia=dia)

            """ query catsim, pack voevents and send """
            iter_and_send(sender, obs_data, obs_metadata, obs_per_field, history)

        """ close connection """
        sender.close()

    else:
        
        session_dir = str(int(time.time()))

        try:
            os.makedirs("json_output/"+session_dir)
        except OSError:
            pass

        for obs_per_field in obs_history:

            """ current observation - largest mjd from a sorted list  """
            obs_metadata = obs_per_field[0]

            obs_data = catsim_utils.catsim_query(stack_version=STACK_VERSION,
                    objid=catsim_table, constraint=catsim_constraint,
                    obs_metadata=obs_metadata, dia=dia)

            """ query catsim and serialize to json  """
            iter_and_serialize(obs_data, obs_metadata, obs_per_field, history, session_dir)


def get_sender(protocol, ipaddr, port, header):
    """ Instantiate proper child class for the given protocol 
    
    @param [in] protocol is name of transmission protocol

    @param [in] ipaddr is IP address of the receiver

    @param [in] port is tcp port of the receiver
    
    @param [in] header is boolean which includes/excludes 4 byte hex header in 
    each VOEvent message (VOEvent standard asks for a header)
    
    @param [out] is object of the broadcast child class
    
    """
    return vars(broadcast)[protocol](ipaddr, port, header)

def iter_and_serialize(obs_data, obs_metadata, observations_field, history, session_dir):

    """ Iterate over catalog and serialize data as JSON, divided
    into files by CCD number
    
    @param [in] obs_data the data from catsim query (one visit)

    @param [in] obs_metadata is the metadata for the given night, 
    or obs_per_field[0], kept for clarity

    @param [in] observations_field is a list of all observations 
    for the given field

    @param [in] history is boolean which determines whether historical 
    occurancies of same DIASource are emitted within each VOEvent
    
    """

    list_of_alert_dicts = []


    if not history:
        for line in obs_data.iter_catalog():
            diaSource_dict = dict(zip(obs_data.iter_column_names(), line))
            alert_dict = {'alertId':45135, 'l1dbId':12545, 
                'diaSource':diaSource_dict}
            list_of_alert_dicts.append(alert_dict)
    else:
        from lsst.sims.catUtils.utils import StellarLightCurveGenerator
        lc_gen = StellarLightCurveGenerator(obs_data.db_obj, '/scratch/veljko/opsim/minion_1016_sqlite.db')

        print("#### real radius")
        ra1=obs_metadata.pointingRA - 1.75
        ra2=obs_metadata.pointingRA + 1.75
        dec1=obs_metadata.pointingDec - 1.75
        dec2=obs_metadata.pointingDec + 1.75

        
        print("ra %f - %f, decl %f - %f" % (ra1, ra2, dec1, dec2))
        pointings = lc_gen.get_pointings((ra1, ra2), (dec1, dec2), expMJD=(0, obs_metadata.mjd.TAI))
        print("number of pointings %d: " % sum(len(x) for x in pointings))
        #import pdb; pdb.set_trace()
        lc_dict, truth_dict = lc_gen.light_curves_from_pointings(pointings)
        #print(lc_dict)
        
        print("#### small radius")
        ra1=obs_metadata.pointingRA - 0.1
        ra2=obs_metadata.pointingRA + 0.1
        dec1=obs_metadata.pointingDec - 0.1
        dec2=obs_metadata.pointingDec + 0.1
        
        print("ra %f - %f, decl %f - %f" % (ra1, ra2, dec1, dec2))
        pointings = lc_gen.get_pointings((ra1, ra2), (dec1, dec2), expMJD=(0, obs_metadata.mjd.TAI))
        print("number of pointings %d: " % sum(len(x) for x in pointings))
        lc_dict, truth_dict = lc_gen.light_curves_from_pointings(pointings)
        #print(lc_dict)
        
        exit(0)
        print("done with lc's")
        print("observations_field len %d" %len(observations_field))
       
        for line in obs_data.iter_catalog():

            print("here")
            diaSource_dict = dict(zip(obs_data.iter_column_names(), line))
            
            diaSource_history = []

            uniqueId = diaSource_dict['diaObjectId']

            lc = lc_dict[uniqueId]

            for filterName, nestedDict in lc.iteritems():
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
                    
                    totFlux = fluxFromMag(totMag)
                    meanFlux = fluxFromMag(meanMag)
                    diaFlux = totFlux - meanFlux

                    # error is not handled yet!!
                    error = nestedDict['error'][i]

                    # remove mags and deltas from other filters

                    list_of_keys = []
                    # copy by value so BANDNAMES remain untouched for the next run
                    otherFilters = BANDNAMES[:]
                    otherFilters.remove(filterName)
                    
                    for name in otherFilters:
                        list_of_keys.append('lsst_%s' % name)
                        list_of_keys.append('delta_lsst_%s' % name)
                    
                    for key in list_of_keys:
                        # remove key from the dict if the key exists
                        temp_dict.pop(key, None)

                    # apply transformations to form diaSource attributes
                    temp_dict['filterName'] = filterName
                    temp_dict['lsst_%s' % filterName] = totMag
                    temp_dict['delta_lsst_%s' % filterName] = totMag - meanMag
                    temp_dict['midPointTAI'] = midPointTai(mjd)
                    #print("obshistid")
                    #print(current_metadata.OpsimMetaData['obsHistID'])
                    # how to get obsHistID?
                    #temp_dict['ccdVisitId'] = ccdVisitId(obsHistID, temp_dict['ccdVisitId'] % 10000)
                    #temp_dict['diaSourceId'] = diaSourceId(
                    temp_dict['apFlux'] = apFlux(diaFlux)
                    diaSource_history.append(temp_dict)

            alert_dict = {'alertId':45135, 'l1dbId':12545, 
                'diaSource':diaSource_dict, 'prv_diaSources':diaSource_history}
            #print(alert_dict)
            list_of_alert_dicts.append(alert_dict)

    avro_utils.catsim_to_avro(list_of_alert_dicts=list_of_alert_dicts, 
            session_dir=session_dir)

def iter_and_send(sender, obs_data, obs_metadata, observations_field, history):

    """ Iterate over catalog and generate XML 

    @param [in] obs_data the data from catsim query (one visit)

    @param [in] obs_metadata is the metadata for the given night, 
    or obs_per_field[0], kept for clarity

    @param [in] observations_field is a list of all observations 
    for the given field

    @param [in] history is boolean which determines whether historical 
    occurancies of same DIASource are emitted within each VOEvent
    """

    event_count = 0
    sending_times = []

    for line in obs_data.iter_catalog():

        # current + historical exposures
        cel_objects = []

        data_metadata = []

        # append metadata to each attribute
        for (val, ucd, unit) in zip(line, obs_data.ucds,
                obs_data.units):
            data_metadata.append(DataMetadata(val, ucd, unit))

        # current exposure with all mags and deltas.
        # will need it for calculating historical variability in
        # different bands.

        cel_obj_all_mags = CelestialObject(obs_data.iter_column_names(),
                data_metadata)

        if (cel_obj_all_mags.varParamStr.value == 'None'):
            print("You should declare varParamStr not like " \
                  "'None' in catsim constraint")
            exit(1)

        cel_obj = deepcopy(cel_obj_all_mags)

        # reduce to a single band
        _remove_band_attrs(cel_obj, obs_metadata.bandpass)
        cel_objects.append(cel_obj)

        # historical exposures can be turned off
        if history:

            base_mags = {}
            for band in BANDNAMES:
                # substract deltas from mags to get base for historical mags
                mag_attr = getattr(cel_obj_all_mags, 'lsst_'+band)
                delta_mag_attr = getattr(cel_obj_all_mags, 'delta_lsst_'+band)
                # other way would be to calculate historical mags
                # via PhotometryStars.
                base_mags[band] = mag_attr.value + delta_mag_attr.value

            for historical_metadata in observations_field:
                vs = VariabilityDummy(historical_metadata)

                # can we get filter-parametrized variabilities
                # from VariabilityMixin please?
                hist_delta_mags = vs.applyVariability(cel_obj_all_mags.varParamStr.value)
                hist_cel_obj = deepcopy(cel_obj_all_mags)

                # not optimal but most flexible for now
                for band in BANDNAMES:
                    hist_mag = base_mags[band] + hist_delta_mags[band]
                    hist_delta_mag = hist_delta_mags[band]
                    _rsetattr(hist_cel_obj, 'lsst_'+band+'.value', hist_mag)
                    _rsetattr(hist_cel_obj, 'delta_lsst_'+band+'.value',
                            hist_delta_mag)

                _remove_band_attrs(hist_cel_obj, historical_metadata.bandpass)
                cel_objects.append(hist_cel_obj)


        # generate and send
        gen = VOEventGenerator(eventid = event_count)
        xml = gen.generateFromObjects(cel_objects, obs_metadata)
        print(xml)
        sender.send(xml)
        event_count += 1
        sending_times.append(time.time())

    # add exception for index out of range
    try:
        sending_diff = sending_times[-1] - sending_times[0]
        print("Number of events from this visit : %d. Time from first to last " \
            "event %f or %f per event" % (event_count, sending_diff,
                    sending_diff/event_count))
    except IndexError:
        print("No events in this visit")


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
