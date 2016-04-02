""" Data model class definitions """


class CelestialObject(object):
    """ A class used to dynamically generate attributes 
        and load data from any db table / catalog        
    """ 

    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value

class DataMetadata(object):
    """ A class used for storing metadata """

    def __init__(self, value=None, ucd=None, unit=None):
        self.value = value
        self.ucd = ucd
        self.unit = unit

