import time
import sqlite3
from generateVOEvent import VOEventGenerator


class Alert(object):
  """ A class describing transient alert objects """
  currentIdNum = 0

  
  def __init__(self, obs_metadata, obj_data):
    self.obs_metadata = obs_metadata # alertObject.obs_metadata.xxx, where xxx = obshistid, site, bandpass, mjd, rotSkyPos
    self.obj_data = obj_data # alertObject.obj_data.yyy, where yyy depend on object type (e.g. raJ2000, decJ2000, lsst_r, lsst_r_var, etc)
    Alert.currentIdNum += 1
    self.alertid = str(obs_metadata.obshistid) + "-" + str(Alert.currentIdNum) # assign unique ID to each Alert object
    self.timestamp=time.time()
    self.status = "Created"
    
  def __lt__(self, other):
    return self.alertid < other.alertid
    
  def convertToVOEvent(self):
    """ Converts alert object to VOEvent format """
    gen = VOEventGenerator(eventid = self.alertid)
    xml = gen.generateFromObjects(self.obj_data, self.obs_metadata)
    return xml
        
  def send(self, sender):
    """ Sends alert object (unicast/multicast/broadcast) """
    voeventMessage=self.convertToVOEvent()
    sender.send(voeventMessage)
        
  def getProperties(self):
    """ Returns dictionary of properties names and values """
    properties=self.__dict__
    return properties
  
  def getSize(self):
    """ Returns the size of the VOEventMessage in bytes """
    size=len(self.convertToVOEvent())
    return size
  
  def writeToDatabase(self, database): # TODO: Works, but too slow for consecutive open/close connections. Optimize.
    """ Writes alert properties to database """
    conn = sqlite3.connect('alerts.db')
    c = conn.cursor()
    alertValues = (self.alertid, self.obs_metadata.obshistid, self.timestamp, self.obj_data.raJ2000.value, self.obj_data.decJ2000.value)
    c.execute('INSERT INTO alerts VALUES (?,?,?,?,?)', alertValues)
    conn.commit()
    conn.close()
    
  def setStatus(self, status):
    """ Sets the status of the alert """
    self.status=status
        
  def getStatus(self):
    """ Gets the status of the alert """
    return self.status
  
  def JDF(self):
    """ Returns JDF of the alert """
    pass
