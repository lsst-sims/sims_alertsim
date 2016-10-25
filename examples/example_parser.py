""" Parse input args and broadcast VOEvents """

import sys
import argparse
import socket
import lsst.sims.alertsim.alertsim_main as alertsim

PARSER = argparse.ArgumentParser(description="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

PARSER.add_argument("-o", "--opsim_table", default="output_opsim3_61",
        help="opsim objid")
PARSER.add_argument("-c", "--catsim_table", default="allstars",
        help="catsim objid")
PARSER.add_argument("-oc", "--opsim_constraint",
        default="night=100",
        help="constraint for opsim query")
PARSER.add_argument("-op", "--opsim_path",
        default="",
        help="your local opsim db path. If left empty fatboy is queried")
PARSER.add_argument("-cc", "--catsim_constraint",
        default="rmag between 10 and 30 and varParamStr not like 'None'",
        help="constraint for catsim query")
#PARSER.add_argument("-ca", "--catsim_catalog",
#        choices=["variable_stars", "vanilla_stars", "DIA_sources", "DIA_objects"],
#        default="variable_stars", help="name of catsim catalog")
PARSER.add_argument("-r", "--radius", type=float, default="1.75",
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
PARSER.add_argument("--no_history",
        help="emit only current events without historical instances",
        action="store_false", default=True)
PARSER.add_argument("--no_dia",
        help="emit basic attributes only, not full DIASources",
        action="store_false", default=True)
PARSER.add_argument("--serialize_json",
        help="doesn't emit VOEvents but serializes them in json format, " \
            "one file per CCD", action="store_true", default=False)
ARGS = PARSER.parse_args()

def validate_ip(ipaddr, protocol):
    
    """ Check validity of ip's and ip/protocol pairings 
    
    @param [in] ipaddr is IP address of the receiver
    
    @param [in] protocol is the protocol used for transmission

    @param [out] boolean inicates whether validation succeeded

    """

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
    #if everything is ok call alertsim.main
    if (validate_ip(ARGS.ipaddress, ARGS.protocol)):
        sys.exit(alertsim.main(ARGS.opsim_table, ARGS.catsim_table,
                ARGS.opsim_constraint, ARGS.opsim_path,
                ARGS.catsim_constraint, ARGS.radius, ARGS.protocol,
                ARGS.ipaddress, ARGS.port, ARGS.no_header,
                ARGS.no_history, ARGS.no_dia, ARGS.serialize_json ))
