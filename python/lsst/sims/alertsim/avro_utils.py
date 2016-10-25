import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from timeit import default_timer as timer
import json


def catsim_to_avro(list_of_query_dicts, schemaURI='avsc/diasource.avsc'):

    """
    Input: list of dictionaries for a catsim visit which consists
    of transformed catsim column_name-value pairs, URI of avsc shema    
    """

    known_schemas = avro.schema.Names()

    diasource_schema = load_avsc_schema("avsc/diasource.avsc", known_schemas)
    ssobject_schema = load_avsc_schema("avsc/ssobject.avsc", known_schemas)
    diaobject_schema = load_avsc_schema("avsc/diaobject.avsc", known_schemas)
    alert_schema = load_avsc_schema("avsc/alert.avsc", known_schemas)

    #alert_schema = avro.schema.parse(open(schemaURI, "rb").read())

    writing_time = timer()
    writer = DataFileWriter(open("avsc/alert.avro", "wb"), DatumWriter(), alert_schema)

    for qd in list_of_query_dicts:

        alert_dict = {'alertID':45135, 'l1dbID':12545, 'diaSource':qd, 'prevDiaSources':[qd]*30}
        json_qd = json.loads(json.dumps(alert_dict))
        print json_qd
        writer.append(json_qd)

    writer.close()
    
    print "writing time %s" % (timer() - writing_time)

    
    #reading_time = timer()
    #reader = DataFileReader(open("diamock.avro", "rb"), DatumReader())
    """
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

    schema_json = json.loads(open(schema_path).read())
    
    schema = avro.schema.make_avsc_object(schema_json, names)

    return schema
    

