import re
import tools.exceptions
from mac_vendor_lookup import MacLookup

MAC_PATTERN = "^\s*([a-z0-9]{6}-[a-z0-9]{6})\s*(\S+)\s*(\d)*$"
MAC_PATTERN_COMPILED = re.compile(MAC_PATTERN)

PORT_PATTERN = "^\s{2}(.{8})\s{1}(.{10})\s{1}(.{7})\s{1}(.{13})\s{1}(.{8})\s{1}(.{10})\s{1}(.{6})\s{1}(.{1,8})"
PORT_PATTERN_COMPILED = re.compile(PORT_PATTERN)

ARP_PATTERN = "^(.{15})\s(.{12})\s*\S*\s*(\S*).*"
ARP_PATTERN_COMPILED = re.compile(ARP_PATTERN)

macLookup = MacLookup()

class MacInfo:
    def __init__(self, text):
        global macLookup
        m = MAC_PATTERN_COMPILED.match(text)
        if not m:
            raise tools.exceptions.InputException
        else:
            self.mac = normalize_mac_two_groups(m.group(1))
            self.port = m.group(2)
            self.vlan = m.group(3)
            self.ip = None
            try:
                self.vendor = macLookup.lookup(self.mac)
            except:
                self.vendor = "UNKNOWN"

    def setIP(self, ip):
        self.ip = ip

class PortInfo:
    def __init__(self, text):
        m = PORT_PATTERN_COMPILED.match(text)
        if not m:
            raise tools.exceptions.InputException
        else:
            self.port = m.group(1).strip()
            self.name = m.group(2).strip()
            self.status = m.group(3).strip()
            self.mode = m.group(4).strip()
            self.speed = m.group(5).strip()
            self.type = m.group(6).strip()
            self.tagged = m.group(7).strip()
            self.untagged = m.group(8).strip()
            self.macs = []

    def addMac(self, mac):
        self.macs.append(mac)

def parse_arp(text):
    m = ARP_PATTERN_COMPILED.match(text)
    if not m:
        raise tools.exceptions.InputException
    else:
        ip = m.group(1).strip()
        mac = normalize_mac_twelve_digits(m.group(2).strip())
        state = m.group(3).strip()
    return mac, ip, state

def normalize_mac_two_groups(mac):
    return "{}:{}:{}:{}:{}:{}".format(mac[0:2], mac[2:4], mac[4:6], mac[7:9], mac[9:11], mac[11:13])

def normalize_mac_twelve_digits(mac):
    return "{}:{}:{}:{}:{}:{}".format(mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])


