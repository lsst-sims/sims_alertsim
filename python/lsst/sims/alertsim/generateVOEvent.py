import sys, os

from lsst.sims.alertsim.VOEventLib import (VOEvent, Who, Author, Citations,
                                           EventIVORN, What, Group, Param,
                                           makeWhereWhen, stringVOEvent)

from astropy.time import Time as AstropyTime

class VOEventGenerator:

    """ A class for generating VOEvent documents.
    Uses VOEventLib by Roy Williams
    """

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
        self.voevent = VOEvent(version=self.voevent_version)
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


    #def generateFromObjects(self, diaSourceData, diaObjectData, obsMetaData):
    def generateFromObjects(self, diaSourcesData, obsMetaData):

        for key, data_tuple in diaSourcesData[0].__dict__.items():
            if data_tuple.ucd == 'pos.eq.ra':
                self.ra = data_tuple.value
            elif data_tuple.ucd == 'pos.eq.dec':
                self.dec = data_tuple.value

        ############ What ############################
        w = What()
#
        for diaSourceData in diaSourcesData:
            g = Group(type_="DIASource", name="DIASource")
            for key, val in diaSourceData.__dict__.items():
                if not key.startswith("__"):
                    p = Param(name=key, ucd=val.ucd, value=val.value, unit = val.unit)
                    g.add_Param(p)
            w.add_Group(g)

        """
        g = Group(type_="DIAObject", name="DIAObject")
        for key, val in diaObjectData.__dict__.items():
            if not key.startswith("__"):
                p = Param(name=key, ucd=val.ucd, value=val.value, unit = val.unit)
                g.add_Param(p)
        w.add_Group(g)
#       """
        self.voevent.set_What(w)

        ############ Wherewhen ############################
        wwd = {'observatory':     self.observatory,
               'coord_system':    'UTC-FK5-GEO',
               'time':            self._convertToIso(obsMetaData.mjd.TAI),
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
               'time':            self._convertToIso(obsMetaData.mjd.TAI),
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
        t = AstropyTime(mjd, format='mjd', scale='tai')
        return t.iso
