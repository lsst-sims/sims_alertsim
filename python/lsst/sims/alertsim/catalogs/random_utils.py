""" Random utils """
import numpy as np

""" Common utilities for catalog classes.
Random number generation, data structure manipulation etc
"""

__all__ = ["rf", "rflist", "ri", "rbi", "array_to_dict"]


def rf():
    """ Returns a random float """
    return np.random.ranf()

def rflist(catalog, count):

    """ List of random floats 

    @param [in] catalog is needed for the number of rows

    @param [in] count is the size of the list

    @param [out] rflist is a list (actually a 2d list)
    of random floats
    """

    return np.random.random_sample((count, len(catalog.column_by_name('simobjid'))))

def ri():
    """ Returns a random integer """
    return np.random.randint(1000)

def rbi():
    """ Returns a random big integer """
    return np.random.randint(0,9223372036854775807)
    
def array_to_dict(cols, vals):
    """ Turns a transposed list of tuples into a dictionary.
    Used for making nested data substructures

    @param [in] cols is a list with names of columns

    @param [in] vals is a transposed list of tuples

    @param [out] list_of_dicts is a list of dictionaries
    """

    list_of_dicts = []
    
    for val in vals:
        dicty = dict(zip(cols, val))
        list_of_dicts.append(dicty)
    return list_of_dicts
