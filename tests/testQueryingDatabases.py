"""
Tests for lsst.sims_alertsim
"""

import unittest
import numpy
import lsst.sims.catalogs.generation.db as catgendb
from lsst.sims.sims_alertsim.alertsim import *


class TestQueryingDatabases(unittest.TestCase):
    ''' Test cases for querying OpSim and CatSim databases;
    Connect to database, perform various queries and generate VO event.
    
    Run this file:> python -m unittest -v testQueryingDatabases
    '''
    
    def test_connectionToDatabase(self):
        ''' Test connection to database '''
        connectedDatabase = catgendb.dbConnection.DBConnection(database='LSSTCATSIM', driver='mssql+pymssql', host='localhost', port='51433' )
        self.assertIsNotNone(connectedDatabase)
    
    def test_opsimQuery(self):
        ''' Test whether exists output from OpSim query '''
        objid = "output_opsim3_61"
        constraint = "obshistid=85163540"
        result = opsim_query_stack10(objid, constraint)
        self.assertIsNotNone(result)

    def test_particularOpsimQueryFor1Visit(self):
        ''' Test OpSim query for one particular visit '''
        objid = "output_opsim3_61"
        constraint = "obshistid=85163540"
        expectedOutput = numpy.array([(85163540, 1.06645, -0.076277, 0.557787, 'i', 49363.058538)], dtype=(numpy.record, [('obshistid', '<i8'), ('fieldra', '<f8'), ('fielddec', '<f8'), ('rawseeing', '<f8'), ('filter', 'S256'), ('expmjd', '<f8')])) # [(85163540, 1.06645, -0.076277, 0.557787, 'i', 49363.058538)]
        self.assertEqual(opsim_query_stack10(objid, constraint), expectedOutput)
    
    def test_catsimQuery(self):
        ''' Test whether exists output from CatSim query '''
        objid = "allstars"
        constraint = "rmag between 20 and 23.5"
        catalog = "variable_stars"
        radius = 0.05
        opsim_metadata = [85163540, 1.06645, -0.076277, 0.557787, 'i', 49363.058538]
        result = catsim_query_stack10(objid, constraint, catalog, radius, opsim_metadata)
        self.assertIsNotNone(result)
        
    def test_catsimQueryDetailed(self):
        ''' Test CatSim query for one particular visit '''
        visit = (85163540, 1.06645, -0.076277, 0.557787, 'i', 49363.058538)
        obj_data, obs_metadata = catsim_query(stack_version=10, 
                objid="allstars", constraint="rmag between 20 and 23.5", 
                catalog="variable_stars", radius=0.05, opsim_metadata=visit)
        self.assertIs(obj_data.__class__.__name__, 'VariableStars')
        self.assertIs(obs_metadata.__class__.__name__, 'ObservationMetaData')
        
    def test_oneObservedObject(self):
        ''' Test result of one observed object '''
        visit = (85163540, 1.06645, -0.076277, 0.557787, 'i', 49363.058538)
        obj_data, obs_metadata = catsim_query(stack_version=10, 
                        objid="allstars", constraint="rmag between 20 and 23.5", 
                        catalog="variable_stars", radius=0.05, opsim_metadata=visit)
        observedObject = obj_data.iter_catalog().next()
        self.assertEqual(observedObject, (820431203, 1.0669846159618328, -0.076030364487934862, 26.051486459463618, 23.537669854192345, 22.258284297509029, 21.124648873258785, 20.603491175400045, 20.35148674548574, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, u'None'))
        
    def test_generateVOEvent(self):
        ''' Test generation of VO event for one observed object '''
        visit = (85163540, 1.06645, -0.076277, 0.557787, 'i', 49363.058538)
        obj_data, obs_metadata = catsim_query(stack_version=10, 
                        objid="allstars", constraint="rmag between 20 and 23.5", 
                        catalog="variable_stars", radius=0.05, opsim_metadata=visit)
        observedObject = obj_data.iter_catalog().next()
        data_metadata = []
        for (val, ucd, unit) in zip(observedObject, obj_data.get_ucds(), obj_data.get_units()):
            data_metadata.append(DataMetadata(val, ucd, unit))
        celestial_object = CelestialObject(obj_data.iter_column_names(), data_metadata)
        gen = VOEventGenerator(eventid = 1)
        xml = gen.generateFromObjects(celestial_object, obs_metadata)
        self.assertEqual(len(xml), 3190)
        
    def test_exceptions(self):
        """ Test that exceptions are raised when they should be """
        
        objid = "output_opsim3_61"
        constraint = "obshistid=85163540"

        # verify that an exception is raised if a nonexisting table is passed to OpSim query
        with self.assertRaises(Exception) as context:
            opsim_query_stack10("FooBarTable", constraint)
        self.assertEqual(context.exception.__class__.__name__, 'NoSuchTableError')
        self.assertEqual('FooBarTable', context.exception.message)
        
        # verify that an exception is raised if insufficient number of arguments is passed to OpSim query
        with self.assertRaises(Exception) as context:
            opsim_query_stack10(objid)
        self.assertEqual(context.exception.__class__.__name__, 'TypeError')
        self.assertTrue('opsim_query_stack10() takes exactly 2 arguments' in context.exception.message)
        
        objid = "allstars"
        constraint = "rmag between 20 and 23.5"
        catalog = "variable_stars"
        radius = 0.05
        opsim_metadata = [85163540, 1.06645, -0.076277, 0.557787, 'i', 49363.058538]

        # verify that an exception is raised if a nonexisting object is passed to CatSim query
        with self.assertRaises(Exception) as context:
            catsim_query_stack10("FooBarObject", constraint, catalog, radius, opsim_metadata)
        self.assertEqual(context.exception.__class__.__name__, 'RuntimeError')
        self.assertEqual('Attempting to construct an object that does not exist', context.exception.message)

        # verify that an exception is raised if a nonexisting catalog is passed to CatSim query
        with self.assertRaises(Exception) as context:
            catsim_query_stack10(objid, constraint, "FooBarCatalog", radius, opsim_metadata)
        self.assertEqual(context.exception.__class__.__name__, 'ValueError')
        self.assertEqual('Unrecognized catalog_type: FooBarCatalog', context.exception.message)
        
        # verify that an exception is raised if insufficient number of arguments is passed to CatSim query
        with self.assertRaises(Exception) as context:
            catsim_query_stack10(objid, constraint, catalog, radius)
        self.assertEqual(context.exception.__class__.__name__, 'TypeError')
        self.assertTrue('catsim_query_stack10() takes exactly 5 arguments' in context.exception.message)
        



if __name__ == '__main__':
    unittest.main()