import sys, os

from VOEventLib import *

from astropy.time import Time as AstropyTime

class VOEventGenerator:

    def __init__(self):
        pass
        #self.v = VOEvent.VOEvent(version="2.0")

    def generateFromObjects(self, objData, obsMetaData, eventID):

        ra = dec = ''

        for key, data_tuple in objData.__dict__.items():
            if data_tuple.ucd == 'pos.eq.ra':
                ra = data_tuple.value
            elif data_tuple.ucd == 'pos.eq.dec':
                dec = data_tuple.value

        ############ VOEvent header ############################
        v = VOEvent.VOEvent(version="2.0")
        v.set_ivorn("ivo://servo.aob.rs/alertsim#%s" % eventID) # v.set_ivorn("ivo://servo.aob.rs/alertsim%s" % objData[0])
        v.set_role("test")
        v.set_Description("")

        ############ Who ############################
        w = Who()
        a = Author()
        a.add_contactName("")
        a.add_contactEmail("")
        w.set_Author(a)
        v.set_Who(w)

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
        v.set_What(w)

        ############ Wherewhen ############################
        wwd = {'observatory':     'LSST CatSim',
               'coord_system':    'UTC-FK5-GEO',
               'time':            self._convertToIso(obsMetaData.mjd),
               'timeError':       0.11,
               'longitude':       ra,
               'latitude':        dec,
               'positionalError': 0.01,
        }

        ww = makeWhereWhen(wwd)
        if ww: v.set_WhereWhen(ww)

        ############ Citation ############################
        c = Citations()
        c.add_EventIVORN(EventIVORN(cite="followup", valueOf_="ivo:lsst.org/resource#89474"))
        c.add_EventIVORN(EventIVORN(cite="followup", valueOf_="ivo:lsst.org/resource#89475"))
        v.set_Citations(c)

        ############ output the event ############################
        xml = stringVOEvent(v,
            schemaURL = "http://www.cacr.caltech.edu/~roy/VOEvent/VOEvent2-110220.xsd")
        return xml

    def generateFromLists(self, cols, vals, ucds):

        ############ VOEvent header ############################
        v = VOEvent.VOEvent(version="2.0")
    #    v.set_ivorn("ivo://silly/billy#%s" % objData[0])
        v.set_role("test")
        v.set_Description("Report of some irrelevant information")

        ############ Who ############################
        w = Who()
        a = Author()
        a.add_contactName("Donald Duck and Goofy")
        a.add_contactEmail("dduck@disney.com")
        w.set_Author(a)
        v.set_Who(w)

        ############ What ############################
        w = What()

        # params related to the event. None are in Groups.
        for col, val, ucd in zip(cols, vals, ucds):
            p = Param(name=col, ucd=ucd, value=val)
           #p.set_Description(["The object ID assigned by the Sillybilly survey"])
            w.add_Param(p)

        # A Group of Params
        g = Group(name="Animals")
        p = Param(name="Tiger", dataType="float", value="1.234")
        g.add_Param(p)
        p = Param(name="Lion",  dataType="float", value="1.234")
        g.add_Param(p)
        w.add_Group(g)
        """
        # event data
        t = Table(name="Event data", Description=[""])
        t.add_Param(Param(name="Random param", ucd="meta.text", value="test"))
        t.add_Field(Field(name="ID"))
        t.add_Field(Field(name="RA"))
        t.add_Field(Field(name="DEC"))
        ut = utilityTable(t)
        ut.blankTable(1)

        ut.setValue("ID",             1, row[0])
        ut.setValue("RA",             1, row[1])
        ut.setValue("DEC",            1, row[2])

        t = ut.getTable()
        w.add_Table(t)
        """
        v.set_What(w)

        ############ Wherewhen ############################
        wwd = {'observatory':     '',
               'coord_system':    'UTC-FK5-GEO',
               'time':            self._convertToIso(obsMetaData.mjd),
               'timeError':       0.11,
               'longitude':       0,
               'latitude':        0,
               'positionalError': 0.01,
        }

        ww = makeWhereWhen(wwd)
        if ww: v.set_WhereWhen(ww)

        ############ Citation ############################
        c = Citations()
        c.add_EventIVORN(EventIVORN(cite="followup", valueOf_="ivo:silly/billy#89474"))
        c.add_EventIVORN(EventIVORN(cite="followup", valueOf_="ivo:silly/billy#89475"))
        v.set_Citations(c)

        ############ output the event ############################
        xml = stringVOEvent(v,
            schemaURL = "http://www.cacr.caltech.edu/~roy/VOEvent/VOEvent2-110220.xsd")
        return xml
    
    def _convertToIso(self, mjd):
        t = AstropyTime(mjd, format='mjd', scale='utc')
        return t.iso
