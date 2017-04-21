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

def _raise_no_avro(method_name):
    msg = "To use %s you must install avro from https://avro.apache.org" % method_name
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

    for alert_dict in list_of_alert_dicts:
        print("Ccd and visit id %d" % (alert_dict['diaSource']['ccdVisitId']))
        
        #last 4 digits of ccdVisitId are chip number
        chipNum = str(alert_dict['diaSource']['ccdVisitId'])[-4:]
        #open file with a name of a chipNum in append mode
        file_obj = open("json_output/"+session_dir+"/"+chipNum, 'a')

        json_qd = json.loads(json.dumps(alert_dict))
        print(json_qd)

        writer.append(json_qd)
        file_obj.close()

    writer.close()

    """
    print "writing time %s" % (timer() - writing_time)

    #reading_time = timer()
    reader = DataFileReader(open("avsc/alert.avro", "rb"), DatumReader())
    
    for line in reader:
        print line
    """

    #print "reading time %s" % (timer() - reading_time)

    #reader.close()

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
    
    schema = avro.schema.make_avsc_object(schema_json, names)

    return schema
    

