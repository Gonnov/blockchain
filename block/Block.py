import hashlib
import datetime as date
from pymerkle import InmemoryTree as MerkleTree

class Block:
    def __init__(self, previous_block: 'Block', \
                transactions, tree: MerkleTree) -> None:
        self.timestamp = date.datetime.now()
        self.transactions = transactions
        self.nonces = 0
        self.merkle_hash = None
    
        if previous_block is None:
            #Index for merkle root is height + 1
            self.height = 0
            self.previous_hash = None
        else:
            self.height = previous_block.height + 1
            self.previous_hash = previous_block.calculate_hash() 
        
    def calculate_hash(self) -> str:
        hash_string = str(self.height) + str(self.timestamp) + str(self.merkle_hash) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()

