from Node.BlockchainNode import BlockchainNode
import time
import requests
from tests.unit.utils import setup_blockchain_n_blocks

# ip = requests.get('https://api.ipify.org').text
ip = ''
gatewayNode = BlockchainNode(ip, 12345, 1)
gatewayNode.blockchain = setup_blockchain_n_blocks(10)
test = BlockchainNode(ip, 12346,2)
# test2 = BlockchainNode(ip, 12347,3)
# test3 = BlockchainNode(ip, 12348,4)
# test4 = BlockchainNode(ip, 12349,5)
# test5 = BlockchainNode(ip, 12350,6)
# test6 = BlockchainNode(ip, 12351,7)
test.debug = True
# gatewayNode.debug = True
gatewayNode.start()
test.start()
# test2.start()
# test3.start()
# test4.start()
# test5.start()
# test6.start()
time.sleep(3)
test.connect_with_node(ip, 12345)
time.sleep(10)
# test2.connect_with_gateway_node(ip, 12345)
# time.sleep(3)
# test3.connect_with_gateway_node(ip, 12345)
# time.sleep(3)
# test4.connect_with_gateway_node(ip, 12345)
# time.sleep(3)
# test5.connect_with_gateway_node(ip, 12345)
# time.sleep(3)
# test6.connect_with_gateway_node(ip, 12345)
# time.sleep(3)
# test6.print_connections()
# print("Gateway Node ->")
# for block in gatewayNode.blockchain.chain:
#     print(block.transactions)
# print("Test Node ->")
# for block in test.blockchain.chain:
#     print(block.transactions)
gatewayNode.stop()
test.stop()
# test2.stop()
# test3.stop()
# test4.stop()
# test5.stop()
# test6.stop()
