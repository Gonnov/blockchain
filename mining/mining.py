from Node.BlockchainNode import BlockchainNode
import time
from transaction.Transaction import Transaction



gatewayNode = BlockchainNode('', 12345, 1)
test = BlockchainNode('', 12346, 2)
gatewayNode.start()
test.start()
time.sleep(5)
test.connect_with_node('', 12345)
time.sleep(5)
gatewayNode.stop()
time.sleep(5)
test.stop()

