from p2pnetwork.node import Node
import requests
import json
from .manageMempool import manageMempool
from .managePeers import managePeers
from .utils import removePeer

class BlockchainNode(Node):
    def __init__(self, host, port,id=None, callback=None, max_connections=0):
        ip = requests.get('https://api.ipify.org').text
        self.peers = [[ip, port]]
        super().__init__(host, port, ip, self.peers, id, callback, max_connections)
        self.port = port
        self.mempool = []

    # all the methods below are called when things happen in the network.
    
    def connect_with_gateway_node(self, ip, port):
        i = 0
        while self.connect_with_node('', port) is False \
            and i < 5: #NEED TO REPLACE IP
            self.connect_with_node('', port)  #NEED TO REPLACE IP
            i += 1

    def outbound_node_connected(self, node):
        pass
        
    def inbound_node_connected(self, node):
        if [node.ip, int(node.port)] not in self.peers:
            self.peers.append([node.ip, int(node.port)])
        i = 0
        while self.connect_with_node('', int(node.port)) is False \
            and i < 5: #NEED TO REPLACE IP
            self.connect_with_node('', int(node.port)) #NEED TO REPLACE IP
            i += 1
        self.send_serialized_data_to_node(node, "peers", self.peers)
        self.send_serialized_data_to_node(node, "mempool", self.mempool)

    def inbound_node_disconnected(self, node):
        removePeer(self, [node.ip, int(node.port)])

    def outbound_node_disconnected(self, node):
        removePeer(self, [node.ip, int(node.port)])


    def node_message(self, node, data):
        if data['type'] == "peers":
            managePeers(self,data['data'])
        elif data['type'] == "mempool":
            manageMempool(self, data['data'])
    
    def send_serialized_data_to_node(self, node, type, data):
        #Used to send data like transaction, mempool, peers...
        data = {
            "type": type,
            "data": data
        }
        serialized_data = json.dumps(data).encode('utf-8')
        self.send_to_node(node, serialized_data)
    
    def node_disconnect_with_outbound_node(self, node):
        removePeer(self, [node.host, int(node.port)])
        
    def node_request_to_stop(self):
        pass
