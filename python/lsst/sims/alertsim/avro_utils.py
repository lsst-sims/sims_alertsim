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

    schema = avro.schema.parse(open(schemaURI, "rb").read())

    writing_time = timer()
    writer = DataFileWriter(open("diamock.avro", "wb"), DatumWriter(), schema)
    
    for qd in list_of_query_dicts:
        """
        writer.append({"diaSourceId": qd["diaSourceId"], 
            "ccdVisitId": qd["ccdVisitId"], "diaObjectId": qd["diaObjectId"], 
            "ssObjectId": qd["ssObjectId"], "midPointTai": 134245.424, 
            "filterName": "u", "radec": {"ra": qd["radec"][0], "decl": qd["radec"][1]}, "apFlux": 14.32})
        """
        with open('avsc/diasource_full.json', 'w') as outfile:
            json.dump(qd, outfile)

        with open('avsc/diasource_full.json') as datafile:
            data = json.load(datafile)

        writer.append(json_qd)
        print qd
        print json_qd
        print data

    writer.close()
    print "writing time %s" % (timer() - writing_time)

    reading_time = timer()
    reader = DataFileReader(open("diamock.avro", "rb"), DatumReader())
    """
    for line in reader:
        print line
    """

    print "reading time %s" % (timer() - reading_time)

    reader.close()
