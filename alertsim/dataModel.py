'''
Data model class definitions
'''

class CelestialObject(object):
    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value

class DataMetadata(object):
    def __init__(self, value=None, ucd=None, unit=None):
        self.value = value
        self.ucd = ucd
        self.unit = unit

