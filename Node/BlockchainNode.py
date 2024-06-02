from p2pnetwork.node import Node
import requests
import json
from Node.dataManager.manageMempool import manageMempool
from Node.dataManager.managePeers import managePeers
from Node.dataManager.manageBlockchain import manageBlockchain

from .utils import removePeer
from  Blockchain.Blockchain import Blockchain
class BlockchainNode(Node):
    """
    Represents a node in the blockchain network.

    Attributes:
        peers (list): List of peer nodes in the network.
        mempool (list): List of pending transactions.
        blockchain (Blockchain): The blockchain managed by the node.
        port (int): The port number on which the node is running.

    Methods:
        connect_with_gateway_node(ip, port): Attempts to connect with a gateway node.
        inbound_node_connected(node): Handles the event when an inbound node connects.
        inbound_node_disconnected(node): Handles the event when an inbound node disconnects.
        outbound_node_disconnected(node): Handles the event when an outbound node disconnects.
        node_message(node, data): Handles messages received from other nodes.
        node_disconnect_with_outbound_node(node): Handles the event when an outbound node disconnects.
        add_transaction_mempool(transaction): Adds a transaction to the mempool if it is valid.
        send_data_to_node(node, type, data): Sends data to a connected node.
    """

    def __init__(self, host: str, port: int, id=None, callback=None, max_connections=0):
        """
        Initializes the BlockchainNode instance.

        Parameters:
            host (str): The host IP address.
            port (int): The port number.
            id (str, optional): The ID of the node. Default is None.
            callback (function, optional): A callback function. Default is None.
            max_connections (int, optional): Maximum number of connections. Default is 0.
        """
        ip = requests.get('https://api.ipify.org').text
        self.peers = [[ip, port]]
        super().__init__(host, port, ip, self.peers, id, callback, max_connections)
        self.port = port
        self.mempool = []
        self.blockchain = Blockchain()
    
    def connect_with_gateway_node(self, ip: str, port: int):
        """
        Attempts to connect with a gateway node up to 5 times.

        Parameters:
            ip (str): The IP address of the gateway node.
            port (int): The port number of the gateway node.
        """
        i = 0
        while self.connect_with_node(ip, port) is False and i < 5:
            i += 1

    def inbound_node_connected(self, node: Node):
        """
        Handles the event when an inbound node connects.

        Parameters:
            node (Node): The inbound node that connected.
        """
        if [node.ip, int(node.port)] not in self.peers:
            self.peers.append([node.ip, int(node.port)])
        i = 0
        while self.connect_with_node(node.ip, int(node.port)) is False and i < 5:
            i += 1
        self.send_data_to_node(node, "peers", self.peers)
        self.send_data_to_node(node, "mempool", self.mempool)
        self.send_data_to_node(node, "blockchain", self.blockchain.chain)

    def inbound_node_disconnected(self, node: Node):
        """
        Handles the event when an inbound node disconnects.

        Parameters:
            node (Node): The inbound node that disconnected.
        """
        removePeer(self, [node.ip, int(node.port)])

    def outbound_node_disconnected(self, node: Node):
        """
        Handles the event when an outbound node disconnects.

        Parameters:
            node (Node): The outbound node that disconnected.
        """
        removePeer(self, [node.ip, int(node.port)])

    def node_message(self, node: Node, data: dict):
        """
        Handles messages received from other nodes.

        Parameters:
            node (Node): The node from which the message was received.
            data (dict): The message data.
        """
        if data['type'] == "peers":
            managePeers(self, data['data'])
        elif data['type'] == "mempool":
            manageMempool(self, data['data'])
        elif data['type'] == "blockchain":
            manageBlockchain(self, data['data'])

    def node_disconnect_with_outbound_node(self, node: Node):
        """
        Handles the event when an outbound node disconnects.

        Parameters:
            node (Node): The outbound node that disconnected.
        """
        removePeer(self, [node.host, int(node.port)])

    def add_transaction_mempool(self, transaction):
        """
        Adds a transaction to the mempool if it is valid.

        Parameters:
            transaction (Transaction): The transaction to add.
        """
        if transaction not in self.mempool:
            if transaction.check_transaction_validity():
                self.mempool.append(transaction)
                self.send_data_to_node(self, "mempool", self.mempool)

    def send_data_to_node(self, node: Node, type: str, data):
        """
        Sends data to a connected node.

        Parameters:
            node (Node): The node to which data is sent.
            type (str): The type of data being sent.
            data (any): The data to send.
        """
        data = {
            "type": type,
            "data": data
        }
        serialized_data = json.dumps(data).encode('utf-8')
        self.send_to_node(node, serialized_data)
