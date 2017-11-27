from __future__ import with_statement
from builtins import zip
import json
import os
import numpy as np

__all__ = ["jsonFromCatalog"]

def jsonFromCatalog(obs_list, cat_class, db, json_dir):

    """
    Parameters
    ----------
    obs_list is a list of ObservationMetaData

    cat_class is the class of InstanceCatalog from which we are generating
    our DIASources

    db is a CatalogDBObject connecting to the database that is the source
    of our DIASources

    json_dir is the directory where we will write out our output
    """

    # taken from
    # https://bugs.python.org/issue24313
    def json_default(o):
        if isinstance(o, np.integer): return int(o)
        raise TypeError("Cannot JSON serialize %s" % o)

    for obs in obs_list:
        source_dict = {}
        cat = cat_class(db, obs_metadata=obs)
        obshistid = obs.OpsimMetaData['obsHistID']
        for data in cat.iter_catalog():
            source = dict(zip(cat._column_outputs, data))
            chipNum = source['ccdVisitId']%10000
            if chipNum>0:
                tag = '%d_%d' % (chipNum, obshistid)
                if tag not in source_dict:
                    source_dict[tag] = []
                source_json = json.dumps(source, default=json_default)
                source_dict[tag].append(source_json)
        for tag in source_dict:
            file_name = os.path.join(json_dir, 'diaSources_%s.txt' % tag)
            with open(file_name, 'w') as file_handle:
                for source in source_dict[tag]:
                     file_handle.write('%s\n' % source)
