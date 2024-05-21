from p2pnetwork.node import Node
import requests
import json
from .manageMempool import manageMempool
from .manageTransaction import manageTransaction
from .managePeers import managePeers

def removePeer(self, peer_to_delete):
    for peer in self.peers:
        if peer[0] == peer_to_delete[0] and peer[1] == peer_to_delete[1]:
            self.peers.remove(peer)
            break

class BlockchainNode(Node):
    def __init__(self, host, port,id=None, callback=None, max_connections=0):
        
        ip = requests.get('https://api.ipify.org').text
        super().__init__(host, port, ip, id, callback, max_connections)
        self.port = port
        self.peers = [[ip, port]]
        self.mempool = []

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        pass
        # self.peers.append([node.ip, node.port])
        # self.send_serialized_data_to_node(node, "peers", self.peers)
        # print("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        self.peers.append([node.ip, int(node.port)])
        self.send_serialized_data_to_node(node, "peers", self.peers)
        # print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        removePeer(self, [node.ip, int(node.port)])
        # print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        removePeer(self, [node.ip, int(node.port)])
        # print("outbound_node_disconnected: (" + self.id + "): " + node.id)


    def node_message(self, node, data):
        # data = json.loads(serialized_data.decode('utf-8'))
        if data['type'] == "peers" and len(self.peers) == 1:
            managePeers(self,data['data'])
        elif data['type'] == "mempool":
            manageMempool(self, data['data'])
        elif data['type'] == "transaction":
            manageTransaction(self, data['data'])
        elif data['type'] == "message":
            print(len(self.peers))
    
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
        # print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        pass
        # print("node is requested to stop (" + self.id + "): ")
