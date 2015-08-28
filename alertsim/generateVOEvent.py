import sys, os

from VOEventLib import *

from astropy.time import Time as AstropyTime

class VOEventGenerator:

    schemaURL = "http://www.cacr.caltech.edu/~roy/VOEvent/VOEvent2-110220.xsd"
    voevent_version = "2.0"
    observatory = "LSST CatSim"

    def __init__(self, eventid, description="", role="test"):
        self.ra = self.dec = ''
        self._initVOEvent(description, role, eventid)
        self.setAuthor(contactName="", contactEmail="")
        self.setCitations()

    def _initVOEvent(self, description, role, eventid):
        ############ VOEvent header ############################
        self.voevent = VOEvent.VOEvent(version=self.voevent_version)
        self.voevent.set_ivorn("ivo://servo.aob.rs/alertsim#%s" % eventid)
        self.voevent.set_role(role)
        self.voevent.set_Description(description)

    def setAuthor(self, contactName, contactEmail):
        ############ Who ############################
        who = Who()
        author = Author()
        author.add_contactName(contactName)
        author.add_contactEmail(contactEmail)
        who.set_Author(author)
        self.voevent.set_Who(who)

    def setCitations(self):
        ############ Citation ############################
        #todo
        c = Citations()
        c.add_EventIVORN(EventIVORN(cite="followup", valueOf_="ivo:lsst.org/resource#89474"))
        c.add_EventIVORN(EventIVORN(cite="followup", valueOf_="ivo:lsst.org/resource#89475"))
        self.voevent.set_Citations(c)


    def generateFromObjects(self, objData, obsMetaData):

        for key, data_tuple in objData.__dict__.items():
            if data_tuple.ucd == 'pos.eq.ra':
                self.ra = data_tuple.value
            elif data_tuple.ucd == 'pos.eq.dec':
                self.dec = data_tuple.value

        ############ What ############################
        w = What()
#        
        g = Group(type_="Magnitudes", name="Magnitudes")
        for key, val in objData.__dict__.items():
            if not key.startswith("__"):
                if val.ucd == 'phot.mag':
                    p = Param(name=key, ucd=val.ucd, value=val.value, unit = val.unit)
#                    p.set_Description(["magnitude"])
#                    p=Param()
#                    p.set_name(key)
#                    p.set_value(float(val.value))
#                    p.set_ucd(val.ucd)
#                    p.set_unit(val.unit)
#                    p.set_dataType("float")
                    g.add_Param(p)
#                    w.add_Param(p)
        w.add_Group(g)
        
        for key, val in objData.__dict__.items():
            if not key.startswith("__"):
                if val.ucd != 'phot.mag':
                    p = Param(name=key, ucd=val.ucd, value=val.value, unit = val.unit)
                    w.add_Param(p)
#       
        #TODO: Obs_metadata contains names and values, so params added manually. Define data model to include ucd and unit.
        
        for key, val in obsMetaData.__dict__.items():
	  if key == "_bandpass":
	    p = Param(name="bandpass", value=val, ucd="instr.bandpass") 
	    w.add_Param(p)
	  if key == "_seeing":
	    p = Param(name="seeing", value=val, dataType="float", ucd="instr.obsty.seeing", unit="arcsec")
	    w.add_Param(p)
	    
	p = Param(name="cutout image", value=None, ucd="obs.image")
	w.add_Param(p)


        self.voevent.set_What(w)

        ############ Wherewhen ############################
        wwd = {'observatory':     self.observatory,
               'coord_system':    'UTC-FK5-GEO',
               'time':            self._convertToIso(obsMetaData.mjd),
               'timeError':       0.11,
               'longitude':       self.ra,
               'latitude':        self.dec,
               'positionalError': 0.01,
        }

        ww = makeWhereWhen(wwd)
        if ww: self.voevent.set_WhereWhen(ww)


        ############ output the event ############################
        xml = stringVOEvent(self.voevent, self.schemaURL)
        return xml

    """
    may be useful at some point, needs to be checked

    def generateFromLists(self, cols, vals, ucds):

        ############ What ############################
        w = What()

        # params related to the event. None are in Groups.
        for col, val, ucd in zip(cols, vals, ucds):
            p = Param(name=col, ucd=ucd, value=val)
           #p.set_Description(["The object ID assigned by the Sillybilly survey"])
            w.add_Param(p)

        self.voevent.set_What(w)

        ############ Wherewhen ############################
        wwd = {'observatory':     self.observatory,
               'coord_system':    'UTC-FK5-GEO',
               'time':            self._convertToIso(obsMetaData.mjd),
               'timeError':       0.11,
               'longitude':       0,
               'latitude':        0,
               'positionalError': 0.01,
        }

        ww = makeWhereWhen(wwd)
        if ww: self.voevent.set_WhereWhen(ww)

        ############ output the event ############################
        xml = stringVOEvent(self.voevent, schemaURL)
        return xml
    
    """

    def _convertToIso(self, mjd):
        t = AstropyTime(mjd, format='mjd', scale='utc')
        return t.iso
