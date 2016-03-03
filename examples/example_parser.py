""" Parse input args and broadcast VOEvents """

import sys
import argparse
import socket
import lsst.sims.sims_alertsim.alertsim.alertsim_main as alertsim

PARSER = argparse.ArgumentParser(description="", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

PARSER.add_argument("-o", "--opsim_table", default="output_opsim3_61",
        help="opsim objid")
PARSER.add_argument("-c", "--catsim_table", default="allstars", 
        help="catsim objid")
PARSER.add_argument("-oc", "--opsim_constraint", 
        default="(night=10 and rawseeing<0.6) and filter like \'i\' ", 
        help="constraint for opsim query")
PARSER.add_argument("-cc", "--catsim_constraint", 
        default="rmag between 20 and 23.5", help="constraint for catsim query")
PARSER.add_argument("-ca", "--catsim_catalog", 
        choices=["variable_stars", "vanilla_stars", "DIA_sources", "DIA_objects"], 
        default="variable_stars", help="name of catsim catalog")
PARSER.add_argument("-r", "--radius", type=float, default="0.05", 
        help="cone search radius")
PARSER.add_argument("-p", "--port", type=int, 
        help="tcp port", default='8098')
PARSER.add_argument("-pr", "--protocol", help="TcpIp, Multicast, Unicast", 
        choices=('TcpIp', 'Multicast', 'Unicast'), default='TcpIp')
PARSER.add_argument("-ip", "--ipaddress", 
        help="ip address of the recepient or multicast channel", 
        default='147.91.240.26')
PARSER.add_argument("--no_header",
        help="don't generate hex header for VOEvents", 
        action="store_false", default=True)
ARGS = PARSER.parse_args()

def validate_ip(ipaddr, protocol):
    """ check validity of ip's and ip/protocol pairings """
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
                print "illegal protocol/ip pair for " \
                "'%s' and '%s'" % (protocol, ipaddr)
                return False
        else:
            if protocol == "Multicast":
                print "illegal protocol/ip pair for " \
                "'%s' and '%s'" % (protocol, ipaddr)
                return False
        return True

if __name__ == "__main__":
    if (validate_ip(ARGS.ipaddress, ARGS.protocol)):
        sys.exit(alertsim.main(ARGS.opsim_table, ARGS.catsim_table, 
                ARGS.opsim_constraint, ARGS.catsim_constraint, 
                ARGS.catsim_catalog, ARGS.radius, ARGS.protocol, 
                ARGS.ipaddress, ARGS.port, ARGS.no_header))
