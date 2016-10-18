from __future__ import with_statement
import xml.etree.ElementTree as ET


def read_and_divide(uri):

    """
    Takes the file outputted by the receiver
    (lsst.sims.alertsim.broadcast.receivers.rec_tcp)
    and returns a list of VOEvents
    """

    voevent_list = []
    voevent = ""
    voevent_flag = False

    with open (uri, 'r') as voevents_file:

        for line in voevents_file:

            if not voevent_flag:
                phrase = "<?xml"
                index = line.find(phrase)
                if index != -1:
                    voevent += line[index:]
                    voevent_flag = True

            else:
                phrase = "</voe:VOEvent>"
                index = line.find(phrase)
                if index != -1:
                    voevent += line[:index+len(phrase)]
                    voevent_list.append(voevent)
                    voevent = ""
                    voevent_flag = False
                else:
                    voevent += line

    return voevent_list

def parse_parameters(ucds, voevent_list):

    """
    Returns a list which contains tuples of values for each ucd
    that was matched in the VOEvent
    """

    data_tuples = []
    for voevent in voevent_list:
        data_tuple = []
        root = ET.fromstring(voevent)
        print root
        for ucd in ucds:
            lines = root.findall("What//Param[@ucd='%s']" % (ucd,))
            for line in lines:
                value = line.attrib["value"]
                data_tuple.append(value)
        data_tuples.append(data_tuple)

    return data_tuples
