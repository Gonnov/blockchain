from Node.BlockchainNode import BlockchainNode
import time
from transaction.Transaction import Transaction
import requests
from user.Wallet import Wallet


def start_server():
    ip = requests.get('https://api.ipify.org').text
    port = int(input("Enter port number: "))
    node = BlockchainNode('', port, 1) #SHOULD BE ip, host, 1
    node.start()
    return node

def connect_with_gateway_node(node):
    gateway_ip = input("Enter gateway ip, if none press enter the blockchain will start independently: ")
    if gateway_ip != '':
        gateway_port = int(input("Enter gateway port: "))
        node.connect_with_gateway_node(gateway_ip, gateway_port)
        time.sleep(10)

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
    i = 0
    while True:
        node.blockchain.mine_block(miner_public_key, i ,node.mempool)
        i += 1
        if i == 4294967295:
            i = 0
        


node = start_server()
connect_with_gateway_node(node)
start_mining(node)
node.stop()
