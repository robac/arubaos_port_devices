from tools.tools import MacInfo
from tools.tools import PortInfo

INPUT_MAC_FILENAME = 'macs.txt'
INPUT_PORT_FILENAME = 'ports.txt'
INPUT_ARP_FILENAME = 'arps.txt'
MAC_IGNORE_TRESHOLD = 5

def read_macs_input(ports):
    input = open(INPUT_MAC_FILENAME, 'r')
    lines = input.readlines()

    count = 0
    for line in lines:
        mac = MacInfo(line)
        if mac.port in ports.keys():
            ports[mac.port].addMac(mac)
        else:
            print("Unknown port: {}".format(mac.port))
    return

def read_macs_input(ports):
    input = open(INPUT_MAC_FILENAME, 'r')
    lines = input.readlines()

    count = 0
    for line in lines:
        mac = MacInfo(line)
        if mac.port in ports.keys():
            ports[mac.port].addMac(mac)
        else:
            print("Unknown port: {}".format(mac.port))
    return


def read_ports_input():
    input = open(INPUT_PORT_FILENAME, 'r')
    lines = input.readlines()
    ports = {}

    count = 0
    for line in lines:
        port = PortInfo(line)
        ports[port.port] = port
    return ports



def main():
    ports = read_ports_input()
    read_macs_input(ports)

    for id, port in ports.items():
        if port.status == "Up":
            print("Port {}".format(port.port))
            if len(port.macs) == 0:
                print("NO MAC ADDRESS")
            elif len(port.macs) > MAC_IGNORE_TRESHOLD:
                print ("TOO MANY ({}) MAC ADDRESSSES".format(len(port.macs)))
            else:
                for mac in port.macs:
                    print("   {}".format(mac.mac))
                    print("   {}".format(mac.vendor))


main()