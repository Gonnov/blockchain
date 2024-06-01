from p2pnetwork.node import Node
import requests
import json
from Node.dataManager.manageMempool import manageMempool
from Node.dataManager.managePeers import managePeers
from Node.dataManager.manageBlockchain import manageBlockchain

from .utils import removePeer
from  Blockchain.Blockchain import Blockchain

class BlockchainNode(Node):
    def __init__(self, host, port,id=None, callback=None, max_connections=0):
        ip = requests.get('https://api.ipify.org').text
        self.peers = [[ip, port]]
        super().__init__(host, port, ip, self.peers, id, callback, max_connections)
        self.port = port
        self.mempool = []
        self.blockchain = Blockchain()
    
    def connect_with_gateway_node(self, ip, port):
        i = 0
        while self.connect_with_node('', port) is False \
            and i < 5: #NEED TO REPLACE IP
            self.connect_with_node('', port)  #NEED TO REPLACE IP
            i += 1
    
    def inbound_node_connected(self, node):
        if [node.ip, int(node.port)] not in self.peers:
            self.peers.append([node.ip, int(node.port)])
        i = 0
        while self.connect_with_node('', int(node.port)) is False \
            and i < 5: #NEED TO REPLACE IP
            self.connect_with_node('', int(node.port)) #NEED TO REPLACE IP
            i += 1
        self.send_data_to_node(node, "peers", self.peers)
        self.send_data_to_node(node, "mempool", self.mempool)
        self.send_data_to_node(node, "blockchain", self.blockchain.chain)

    def inbound_node_disconnected(self, node):
        removePeer(self, [node.ip, int(node.port)])

    def outbound_node_disconnected(self, node):
        removePeer(self, [node.ip, int(node.port)])

    def node_message(self, node, data):
        if data['type'] == "peers":
            managePeers(self,data['data'])
        elif data['type'] == "mempool":
            manageMempool(self, data['data'])
        elif data['type'] == "blockchain":
            manageBlockchain(self, data['data'])

    def node_disconnect_with_outbound_node(self, node):
        removePeer(self, [node.host, int(node.port)])
    
    def add_transaction_mempool(self, transaction):
        if transaction not in self.mempool:
            if transaction.check_transaction_validity():
                self.mempool.append(transaction)
                self.send_data_to_node(self, "mempool", self.mempool)

    def send_data_to_node(self, node, type, data):
        #Used to send data like transaction, mempool, peers...
        data = {
            "type": type,
            "data": data
        }
        serialized_data = json.dumps(data).encode('utf-8')
        self.send_to_node(node, serialized_data)