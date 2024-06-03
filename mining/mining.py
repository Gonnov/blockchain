from Node.BlockchainNode import BlockchainNode
import time
from transaction.Transaction import Transaction
import requests
from user.Wallet import Wallet


def start_server():
    ip = requests.get('https://api.ipify.org').text
    port = input("Enter port number (should be > 1024 or < 49151, default 12345): ")
    try:
        port = int(port)
        if port < 1024 or port > 49151:
            print("Invalid port number, using default port number 12345")
            port = 12345
    except:
        print("Invalid port number, using default port number 12345")
        port = 12345
    node = BlockchainNode('', port, 1) #SHOULD BE ip, host, 1
    node.start()
    return node

def connect_with_gateway_node(node):
    gateway_ip = input("Enter gateway ip, if none press enter the blockchain will start independently: ")
    if gateway_ip != '':
        gateway_port = int(input("Enter gateway port: "))
        print("Connecting to the network...")
        node.connect_with_gateway_node(gateway_ip, gateway_port)
        time.sleep(10)
        print("Connected to the network")

def get_miner_public_key():
    miner_public_key = input("Enter your public key or press enter to generate one: ")
    if miner_public_key == '':
        miner_wallet = Wallet()
        miner_public_key = miner_wallet.get_public_key_hex()
        print("Your public key is: ", miner_public_key)
        print("Your private key is: ", miner_wallet.get_private_key_hex())
        print("Please keep a copy of these 2 keys or at least the private key to access your wallet later.")
        print("The blockchain will not keep your private key for security reasons.")
    return miner_public_key

def start_mining(node):
    miner_public_key = get_miner_public_key()
    print("Mining started")
    i = 0
    while True:
        node.blockchain.start_mining(miner_public_key, 0, node.mempool)
        print("Block mined")
        node.send_data_to_all_nodes("new block", node.blockchain.chain[-1])
        

        


node = start_server()
connect_with_gateway_node(node)
start_mining(node)
node.stop()
