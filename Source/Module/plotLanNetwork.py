#File Import
import pcapReader
import communicationDetailsFetch
import torTrafficHandle
import maliciousTrafficIdentifier

import networkx as nx
import matplotlib.pyplot as plt

from graphviz import Digraph
import threading

class plotLan:

    def __init__(self, packetDB, filename, name_servers, option="Tor"):
        self.packetDB = packetDB
        self.filename = filename+option

        self.styles = {
            'graph': {
                'label': 'PcapGraph',
                'fontsize': '16',
                'fontcolor': 'black',
                'bgcolor': 'grey',
                'rankdir': 'BT',
                'dpi':'300'
            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'circle',
                'fontcolor': 'black',
                'color': ' black',
                'style': 'filled',
                'fillcolor': 'yellow',
            }
        }

        self.nodes = self.packetDB.keys()
        self.name_servers = name_servers
        #communicationDetailsFetch.trafficDetailsFetch(self.packetDB).communication_details
        if option == "Malicious" or option == "All":
            self.mal_identify = maliciousTrafficIdentifier.maliciousTrafficIdentifier(self.packetDB, self.name_servers).possible_malicious_traffic
        if option == "Tor" or option == "All":
            self.tor_identify = torTrafficHandle.torTrafficHandle(self.packetDB).possible_tor_traffic
        self.draw_graph(option)
    
    def apply_styles(self, graph, styles):
        graph.graph_attr.update(
            ('graph' in styles and styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in styles and styles['nodes']) or {}
        )
        return graph

    def apply_custom_style(self, graph, color):
        style = {'edges': {
                'style': 'dashed',
                'color': color,
                'arrowhead': 'open',
                'fontname': 'Courier',
                'fontsize': '12',
                'fontcolor': color,
        }}
        graph.edge_attr.update(
            ('edges' in style and style['edges']) or {}
        )
        return graph

    def draw_graph(self,option="All"):
        f = Digraph('network_diagram - '+option, filename=self.filename, engine="dot", format="png")
        f.attr(rankdir='LR', size='8,5')

        f.attr('node', shape='doublecircle')
        f.node('defaultGateway')

        f.attr('node', shape='circle')

        print "Starting Graph Plotting"

        if option == "All":
            # add nodes
            for node in self.nodes:
                f.node(node)
                if "TCP" in self.packetDB[node]:
                    if "HTTPS" in self.packetDB[node]["TCP"]:
                        for dest in self.packetDB[node]["TCP"]["HTTPS"]:
                            f.edge(node, 'defaultGateway', label='HTTPS: ' +dest+": "+self.name_servers[node]["ip_details"][dest]["dns"], color = "blue")
                    if "HTTP" in self.packetDB[node]["TCP"]:
                        for dest in self.packetDB[node]["TCP"]["HTTP"]["Server"]:
                            f.edge(node, 'defaultGateway', label='HTTP: ' + dest+": "+self.name_servers[node]["ip_details"][dest]["dns"], color = "green")
                    for tor in self.tor_identify[node]:
                       f.edge(node, 'defaultGateway', label='TOR: ' + str(tor) ,color="white")

                    for mal in self.mal_identify[node]:
                        f.edge(node, 'defaultGateway', label='MaliciousTraffic: ' + str(mal), color="red")


        if option == "HTTP":
            for node in self.nodes:
                f.node(node)
                if "TCP" in self.packetDB[node]:
                    if "HTTP" in self.packetDB[node]["TCP"]:
                        for dest in self.packetDB[node]["TCP"]["HTTP"]["Server"]:
                            f.edge(node, 'defaultGateway', label='HTTP: ' + dest + ": " + self.name_servers[node]["ip_details"][dest]["dns"],color="green")

        if option == "HTTPS":
            for node in self.nodes:
                f.node(node)
                if "TCP" in self.packetDB[node]:
                    if "HTTPS" in self.packetDB[node]["TCP"]:
                        for dest in self.packetDB[node]["TCP"]["HTTPS"]:
                            f.edge(node, 'defaultGateway', label='HTTPS: ' +dest+": "+self.name_servers[node]["ip_details"][dest]["dns"], color = "blue")

        if option == "Tor":
            for node in self.nodes:
                f.node(node)
                for tor in self.tor_identify[node]:
                    f.edge(node, 'defaultGateway', label='TOR: ' + str(tor), color="white")

        if option == "Malicious":
            for node in self.nodes:
                f.node(node)
                for mal in self.mal_identify[node]:
                    f.edge(node, 'defaultGateway', label='MaliciousTraffic: ' + str(mal), color="red")


        self.apply_styles(f,self.styles)
        f.render()


def main():
    # draw example
    pcapfile = pcapReader.pcapReader('test.pcap')
    print "Reading Done...."
    network = plotLan(pcapfile.packetDB, "network12345", "All")

#main()
