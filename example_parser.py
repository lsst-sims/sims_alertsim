""" Parse input args and broadcast VOEvents """

import sys
import os
import argparse
import socket
from alertsim import *

def main(opsim_table, catsim_table, opsim_constraint, 
         catsim_constraint, catalog, radius, protocol, ipaddr, port):

    """ Take objids, constraints and metadata, query
        opsim and catsim and generate VOevents 
    """
    sender = get_sender(protocol, ipaddr, port)
    if os.environ['SETUP_OBS_LSSTSIM'][12] == '8':
        observations = opsim_query(objid=opsim_table, 
            constraint=opsim_constraint)
    else:
        dbadr = "mssql+pymssql://LSST-2:L$$TUser@fatboy.npl.washington.edu:1433/LSST" 

        observations = opsim_query_stack10(dbadr, 
            constraint=opsim_constraint)
 
    for obs in observations:
        if os.environ['SETUP_OBS_LSSTSIM'][12] == '8':
            t, obs_metadata = catsim_query(catsim_table, catsim_constraint, 
                catalog, radius, obs)
        else:
            t, obs_metadata = catsim_query_stack10(catsim_table, catsim_constraint, 
                                                   catalog, radius, obs)
 
        iter_and_send(sender, t, obs_metadata)

PARSER = argparse.ArgumentParser(description="")

PARSER.add_argument("-o", "--opsim_table", default="opsim3_61", 
        help="opsim objid")
PARSER.add_argument("-c", "--catsim_table", default="allstars", 
        help="catsim objid")
PARSER.add_argument("-oc", "--opsim_constraint", 
        default="(night=10 and rawseeing<0.6) and filter like \'i\' ", 
        help="constraint for opsim query")
PARSER.add_argument("-cc", "--catsim_constraint", 
        default="rmag between 20 and 23.5", help="constraint for catsim query")
PARSER.add_argument("-ca", "--catsim_catalog", 
        choices=["variable_stars", "vanilla_stars"], 
        default="variable_stars", help="name of catsim catalog")
PARSER.add_argument("-r", "--radius", type=float, default="0.05", 
        help="cone search radius")
PARSER.add_argument("-p", "--port", type=int, help="tcp port", default='8098')
PARSER.add_argument("-pr", "--protocol", help="TcpIp, Multicast, Unicast", 
        choices=('TcpIp', 'Multicast', 'Unicast'), default='TcpIp')
PARSER.add_argument("-ip", "--ipaddress", 
        help="ip address of the recepient or multicast channel", 
        default='147.91.240.26')
ARGS = PARSER.parse_args()

def validate_ip(ipaddr, protocol):
    try:
    #check if ip is valid
        socket.inet_aton(ipaddr)
    except socket.error:
        print "illegal ip '%s'" % ipaddr
        return False
    else: 
    #check if multicast is assigned to right ip and vice versa    
        ipbase = ipaddr[:3].split(".")[0]
        if (224 <= int(ipbase) <= 239):
            if protocol != "Multicast":
                print "illegal protocol/ip pair for '%s' and '%s'" % (protocol, ipaddr)
                return False
        else:
            if protocol == "Multicast":
                print "illegal protocol/ip pair for '%s' and '%s'" % (protocol, ipaddr)
                return False
        return True


if __name__ == "__main__":
    if (validate_ip(ARGS.ipaddress, ARGS.protocol)):
        sys.exit(main(ARGS.opsim_table, ARGS.catsim_table, ARGS.opsim_constraint, 
                    ARGS.catsim_constraint, ARGS.catsim_catalog, ARGS.radius, 
                    ARGS.protocol, ARGS.ipaddress, ARGS.port))
