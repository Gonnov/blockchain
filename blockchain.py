from block.Block import Block
from transaction.Transaction import Transaction
from transaction.CoinbaseTransaction import CoinbaseTransaction

from pymerkle import InmemoryTree as MerkleTree
from pymerkle import verify_consistency, verify_inclusion
import pickle

class Blockchain:
    def __init__(self) -> None:
        self.tree = MerkleTree(algorithm='sha256')
        self.difficulty = 4
        self.coinbase_value = 50
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self) -> None:
        transactions = [None]
        block = Block(None, transactions, self.tree)
        merkle_index = self.tree.append_entry(pickle.dumps(block.transactions))
        block.merkle_hash = self.tree.get_leaf(merkle_index)
        return block
    
    def mine_block(self, miner_address, extra_nonce) -> None:
        #NEED TO ADD THE TRANSACTIONS FROM THE MEMPOOL
        coinbase_transaction = CoinbaseTransaction(self.coinbase_value, miner_address, extra_nonce)
        block = Block(self.chain[-1], coinbase_transaction, self.tree)
        difficulty_string = '0' * self.difficulty
        if block.calculate_hash()[:self.difficulty] != difficulty_string:
            if block.nonces == 4294967295:
                block.nonces = 0
            else:
                block.nonces += 1
            return False
        else:
            #NEED TO ADD THE TRANSACTIONS FROM THE MEMPOOL
            self.add_block(block.transactions)
    
    def add_block(self, transactions: Transaction) -> None:
        block = Block(self.chain[-1], transactions, self.tree)
        merkle_index = self.tree.append_entry(pickle.dumps(block.transactions))
        block.merkle_hash = self.tree.get_leaf(merkle_index)
        self.chain.append(block)
        
    def check_whole_blocks(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.previous_hash != previous_block.calculate_hash():
                return False
        return True
    
    def check_consistency_single_block(self, block_height: int) -> None:
        merkle_index = block_height + 1
        proof = self.tree.prove_consistency(1, merkle_index)
        first_state = self.tree.get_state(1)
        last_state = self.tree.get_state(merkle_index)
        verify_consistency(first_state, last_state, proof)
    
    def check_consistency_tree(self) -> None:
        proof = self.tree.prove_consistency(1, len(self.chain))
        first_state = self.tree.get_state(1)
        last_state = self.tree.get_state()
        verify_consistency(first_state, last_state, proof)
    
    def check_inclusion_single_block(self, block_height: int) -> None:
        proof = self.tree.prove_inclusion(block_height + 1, len(self.chain))
        first_state = self.tree.get_leaf(block_height + 1)
        last_state = self.tree.get_state(len(self.chain))
        verify_inclusion(first_state, last_state, proof)
    
    def check_inclusion_tree(self) -> None:
        last_state = self.tree.get_state(len(self.chain))
        for i in range(0, len(self.chain)):
            proof = self.tree.prove_inclusion(self.chain[i].height + 1, len(self.chain))
            first_state = self.tree.get_leaf(self.chain[i].height + 1)
            verify_inclusion(first_state, last_state, proof)
        
    def get_block(self, block_height: int) -> Block:
        return self.chain[block_height]

    