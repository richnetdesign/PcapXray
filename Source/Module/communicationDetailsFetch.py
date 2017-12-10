# Library Import
import ipwhois
import dns
import socket
import Queue
# Module Import
import pcapReader
import netaddr

# Class Communication or Traffic Details Fetch

class trafficDetailsFetch():

    def __init__(self, packetDB, out):
        self.communication_details = {}
        for ip in packetDB:
            if ip not in self.communication_details:
                self.communication_details[ip] = {}
            ips = []
            if "TCP" in packetDB[ip] and "PortsConnected" in packetDB[ip]["TCP"]:
                for entry in packetDB[ip]["TCP"]["PortsConnected"]:
                        ips.append(entry[0])
            if "UDP" in packetDB[ip] and "PortsConnected" in packetDB[ip]["UDP"]:
                for entry in packetDB[ip]["UDP"]["PortsConnected"]:
                        ips.append(entry[0])
            if "ip_details" not in self.communication_details[ip]:
                self.communication_details[ip]["ip_details"] = {}
            self.communication_details[ip]["ip_details"] = {key: {} for key in ips}
            self.dns(ip, self.communication_details[ip]["ip_details"].keys())
        out.put(self.communication_details)
            #self.whois_info_fetch(ip, self.communication_details[ip]["ip_details"].keys())

    # whois_info_fetch
    #        - Input    : Domain Name and IP address
    #        - Function : Obtains the Whois Information for the given domain or IP
    #                      * Domain
    #                      * Leverages restApi with "whois.com/whois" api call
    #                      * IP
    #                      * Leverages the ipWhois python library to fetch info
    #        - Output   : Returns the whois data obtained from whois.com and ipwhois
    #
    def whois_info_fetch(self, ip, ips):
       for i in ips:
         if "whois" not in self.communication_details[ip]["ip_details"][i]:
             self.communication_details[ip]["ip_details"][i]["whois"] = ""
         try:
            whois_info = ipwhois.IPWhois(ip).lookup_rdap()
         except:
            whois_info = "NoWhoIsInfo"
         self.communication_details[ip]["ip_details"][i]["whois"] = whois_info

    def dns(self, ip, ips):
        for i in ips:
            if "dns" not in self.communication_details[ip]["ip_details"][i]:
                self.communication_details[ip]["ip_details"][i]["dns"] = ""
            try:
                dns_info = socket.gethostbyaddr(i)[0]
            except:
                dns_info = "NotResolvable"
            self.communication_details[ip]["ip_details"][i]["dns"] = dns_info

def main():
    out1 = Queue.Queue()
    capture = pcapReader.pcapReader("lanExample.pcap", out1)
    print "read"
    out = Queue.Queue()
    details = trafficDetailsFetch(out1.get(), out)
    print out.get()
    print "\n"

#main()
