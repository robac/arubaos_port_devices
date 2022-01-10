import re
import tools.exceptions
from mac_vendor_lookup import MacLookup

MAC_PATTERN = "^\s*([a-z0-9]{6}-[a-z0-9]{6})\s*(\S+)\s*(\d)*$"
MAC_PATTERN_COMPILED = re.compile(MAC_PATTERN)

PORT_PATTERN = "^\s{2}(.{8})\s{1}(.{10})\s{1}(.{7})\s{1}(.{13})\s{1}(.{8})\s{1}(.{10})\s{1}(.{6})\s{1}(.{1,8})"
PORT_PATTERN_COMPILED = re.compile(PORT_PATTERN)

macLookup = MacLookup()

class MacInfo:
    def __init__(self, text):
        global macLookup
        m = MAC_PATTERN_COMPILED.match(text)
        if not m:
            raise tools.exceptions.InputException
        else:
            self.mac = normalize_mac(m.group(1))
            self.port = m.group(2)
            self.vlan = m.group(3)
            try:
                self.vendor = macLookup.lookup(self.mac)
            except:
                self.vendor = "UNKNOWN"

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



def normalize_mac(mac):
    return "{}:{}:{}:{}:{}:{}".format(mac[0:2], mac[2:4], mac[4:6], mac[7:9], mac[9:11], mac[11:13])


