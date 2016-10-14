import lsst.sims.alertsim.alertsim_main as alertsim
import os

    def testReceiver(self):
        alertsim.main(opsim_table = "", catsim_table = "test_allstars",
            opsim_constraint = "night = 100", opsim_path = "",
            catsim_constraint = "varParamStr not like 'None'",
            radius = "1.75", protocol = "TcpIp", ipaddr="localhost",
            port = "8080", header = False, history = False, dia = False)

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../python/sims/alertsim/broadcast/receivers/VOEvents.txt")
        voevent_list = read_and_divide(filename)
        ucds = ["pos.eq.ra", "pos.eq.dec", "phot.mag"]
        voevent_data_tuples = parse_parameters(ucds, voevent_list)
