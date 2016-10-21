import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

def catsim_to_avro(schemaURI='avsc/diamock.avsc', qd):
    
    """
    Input: URI of the avro schema, query dictionary (qd) which consists
    of transformed catsim column_name-value pairs 
    """

    schema = avro.schema.parse(open(schemaURI, "rb").read())

    writer = DataFileWriter(open("diamock.avro", "wb"), DatumWriter(), schema)
    writer.append({"diaSourceId": qd[diaSourceId], "midPointTai": 134245.424, 
        "filterName": "u", "radec": {"ra": qd[radec[0], "decl": dq[radec[1]}, "apFlux": 14.32})
    writer.close()

    reader = DataFileReader(open("diamock.avro", "rb"), DatumReader())
    for user in reader:
            print user
            reader.close()
