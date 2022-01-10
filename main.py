from tools.tools import MacInfo
from tools.tools import PortInfo
from tools.tools import parse_arp

INPUT_MAC_FILENAME = 'data\\macs.txt'
INPUT_PORT_FILENAME = 'data\\ports.txt'
INPUT_ARP_FILENAME = 'data\\arps.txt'
MAC_IGNORE_TRESHOLD = 5

def read_macs_input(ports, arps):
    input = open(INPUT_MAC_FILENAME, 'r')
    lines = input.readlines()

    for line in lines:
        mac = MacInfo(line)
        if mac.mac in arps.keys():
            mac.setIP(arps[mac.mac])
        if mac.port in ports.keys():
            ports[mac.port].addMac(mac)
        else:
            print("Unknown port: {}".format(mac.port))
    return

def read_arps_input():
    input = open(INPUT_ARP_FILENAME, 'r')
    lines = input.readlines()
    arps = {}

    for line in lines:
        mac, ip, state = parse_arp(line)
        if (state in ['VLD', 'STS']):
            arps[mac] = ip
    return arps


def read_ports_input():
    input = open(INPUT_PORT_FILENAME, 'r')
    lines = input.readlines()
    ports = {}

    for line in lines:
        port = PortInfo(line)
        ports[port.port] = port
    return ports


def print_ports(ports):
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
                    print("     {}".format(mac.vendor))
                    if mac.ip is None:
                        print("     IP unknown")
                    else:
                        print("     IP: {}".format(mac.ip))

    return

def main():
    arps = read_arps_input()
    ports = read_ports_input()
    read_macs_input(ports, arps)

    print_ports(ports)


main()