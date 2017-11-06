from __future__ import print_function
try:
    import avro.schema
    from avro.datafile import DataFileReader, DataFileWriter
    from avro.io import DatumReader, DatumWriter
    _avro_installed = True
except:
    _avro_installed = False

from timeit import default_timer as timer
import json
import numpy as np
from collections import defaultdict

def _raise_no_avro(method_name):
    msg = "To use %s you must install avro-python3 from https://avro.apache.org. You might use pip install avro-python3" % method_name
    raise RuntimeError(msg)


def catsim_to_avro(list_of_alert_dicts, session_dir, schemaURI='avsc/diasource.avsc'):

    """
    Input: list of dictionaries for a catsim visit which consists
    of transformed catsim column_name-value pairs, URI of avsc shema    
    """
    global _avro_installed
    if not _avro_installed:
        _raise_no_avro("catsim_to_avro")

    known_schemas = avro.schema.Names()

    diasource_schema = load_avsc_schema("avsc/diasource.avsc", known_schemas)
    ssobject_schema = load_avsc_schema("avsc/ssobject.avsc", known_schemas)
    diaobject_schema = load_avsc_schema("avsc/diaobject.avsc", known_schemas)
    alert_schema = load_avsc_schema("avsc/alert.avsc", known_schemas)

#    alert_schema = avro.schema.parse(open(schemaURI, "rb").read())

    writing_time = timer()
    writer = DataFileWriter(open("avsc/alert.avro", "wb"), DatumWriter(), alert_schema)

    print("number of events %d" % (len(list_of_alert_dicts)))

    alert_dicts_divided = defaultdict(list)
    for d in list_of_alert_dicts:
        alert_dicts_divided[(d['diaSource']['ccdVisitId'])].append(d)
    
    print("##### starting serialization")

    for ix, list_per_chip in enumerate(alert_dicts_divided.values()):
        print("Ccd and visit id %d" % (list_per_chip[0]['diaSource']['ccdVisitId']))
        #last 4 digits of ccdVisitId are chip number
        chipNum = str(list_per_chip[0]['diaSource']['ccdVisitId'])[-4:]

        serialization_timer = timer()

        #open file with a name of a chipNum in append mode
        file_obj = open("json_output/"+session_dir+"/"+chipNum, 'a')
        
        avro_validated = False

        for alert_dict in list_per_chip:
            
            # json cannot serialize numpy types
            #print("before scalarize")
            #print(_print_types(alert_dict))
            #_numpy_to_scalar(alert_dict)
            #print("after scalarize")
            #print(_print_types(alert_dict))

            json.dump(alert_dict, file_obj)

            if (ix==0 and avro_validated==False):
            
                writer.append(alert_dict)
                print("Avro schema validated for this chunk")
                avro_validated = True

        file_obj.close()
        print("serialization for %d events on this chip took %s" % (len(list_per_chip), timer()-serialization_timer))

    writer.close()

    print("total serialization time for this chunk is %s" % (timer() - writing_time))

    """
    #reading_time = timer()
    reader = DataFileReader(open("avsc/alert.avro", "rb"), DatumReader())
    
    for line in reader:
        print line

    print "reading time %s" % (timer() - reading_time)

    reader.close()
    """

def load_avsc_schema(schema_path, names = None):
    
    """ Load avsc file

    @param [in] schema_path is file path to the schema file

    @param [in] names is avro.schema.Names object, required for nested schemas

    @param [out] schema is avro schema

    """
    global _avro_installed
    if not _avro_installed:
        _raise_no_avro("load_avsc_schema")


    schema_json = json.loads(open(schema_path).read())
    
    #schema = avro.schema.make_avsc_object(schema_json, names)
    schema = avro.schema._SchemaFromJSONObject(schema_json, names)

    return schema
    

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

def _print_types(d, types = []):
    for k, v in d.items():
        if isinstance(d[k], dict):
            _print_types(d[k], types)
        else:
            types.append([k, type(v)])
    return types
