from Block.Block import Block
from transaction.Transaction import Transaction
from transaction.CoinbaseTransaction import CoinbaseTransaction
from pymerkle import InmemoryTree as MerkleTree
from pymerkle import verify_consistency, verify_inclusion
import pickle

class Blockchain:
    def __init__(self) -> None:
        """
        Initialize the Blockchain.

        Initializes the blockchain with a Merkle tree, sets the mining difficulty,
        assigns the coinbase value, and creates the genesis block.
        """
        self.tree = MerkleTree(algorithm='sha256')
        self.difficulty = 4
        self.coinbase_value = 50
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self) -> None:
        """
        Create the genesis block.

        Returns:
            Block: The genesis block.
        """
        transactions = [None]
        block = Block(None, transactions, self.tree)
        merkle_index = self.tree.append_entry(pickle.dumps(block.transactions))
        block.merkle_hash = self.tree.get_leaf(merkle_index)
        return block
    
    def mine_block(self, miner_address, extra_nonce) -> None:
        """
        Mine a new block.

        Args:
            miner_address: The address of the miner who mines the block.
            extra_nonce: Extra nonce value for mining.

        Returns:
            bool: True if the block is successfully mined, False otherwise.
        """
        #NEED TO ADD THE TRANSACTIONS FROM THE MEMPOOL
        coinbase_transaction = CoinbaseTransaction(self.coinbase_value, miner_address)
        block = Block(self.chain[-1], coinbase_transaction, self.tree)
        difficulty_string = '0' * self.difficulty
        if block.calculate_hash()[:self.difficulty] != difficulty_string: #NEED TO PUT A DIFFICULTY ALGORITHM
            if block.nonces == 4294967295:
                block.nonces = 0
            else:
                block.nonces += 1
            return False
        else:
            #NEED TO ADD THE TRANSACTIONS FROM THE MEMPOOL
            self.add_block(block.transactions)
    
    def add_block(self, transactions: Transaction) -> None:
        """
        Add a new block to the blockchain.

        Args:
            transactions: The transactions to be added to the block.
        """
        block = Block(self.chain[-1], transactions, self.tree)
        merkle_index = self.tree.append_entry(pickle.dumps(block.transactions))
        block.merkle_hash = self.tree.get_leaf(merkle_index)
        self.chain.append(block)
        
    def check_whole_blocks(self) -> bool:
        """
        Check the integrity of the entire blockchain.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.previous_hash != previous_block.calculate_hash():
                return False
        return True
    
    def check_consistency_single_block(self, block_height: int) -> None:
        """
        Verify the consistency of a specific block within the blockchain.

        Args:
            block_height (int): The height of the block to check consistency for.

        Generates a consistency proof for the blockchain up to the specified block
        height and verifies that the state transitions from the first block to this
        block are valid.
        """
        merkle_index = block_height + 1
        proof = self.tree.prove_consistency(1, merkle_index)
        first_state = self.tree.get_state(1)
        last_state = self.tree.get_state(merkle_index)
        try:
            verify_consistency(first_state, last_state, proof)
            return True
        except:
            return False
    
    def check_consistency_tree(self) -> None:
        """
        Verify the consistency of the entire blockchain tree.
        
        Generates a consistency proof for the blockchain from the first block 
        to the current state, and verifies that the state transitions are valid.
        """
        proof = self.tree.prove_consistency(1, len(self.chain))
        first_state = self.tree.get_state(1)
        last_state = self.tree.get_state()
        try:
            verify_consistency(first_state, last_state, proof)
            return True
        except:
            return False
    
    def check_inclusion_single_block(self, block_height: int) -> None:
        """
        Verify that the block at the given height is included in the blockchain using a Merkle tree inclusion proof.
        
        Args:
            block_height (int): The height of the block to verify.

        Process:
            1. Generate an inclusion proof for the block.
            2. Retrieve the hash of the specified block (leaf node).
            3. Retrieve the root hash of the Merkle tree (blockchain state).
            4. Verify the inclusion proof to ensure the block is part of the blockchain.
        """
        proof = self.tree.prove_inclusion(block_height + 1, len(self.chain))
        first_state = self.tree.get_leaf(block_height + 1)
        last_state = self.tree.get_state(len(self.chain))
        try:
            verify_inclusion(first_state, last_state, proof)
            return True
        except:
            return False
    
    def check_inclusion_tree(self) -> None:
        """
        Verify that all blocks in the blockchain are included using Merkle tree inclusion proofs.
        
        Process:
            1. Retrieve the root hash of the Merkle tree (blockchain state).
            2. For each block in the blockchain:
            a. Generate an inclusion proof for the block.
            b. Retrieve the hash of the block (leaf node).
            c. Verify the inclusion proof to ensure the block is part of the blockchain.
        """
        last_state = self.tree.get_state(len(self.chain))
        for i in range(0, len(self.chain)):
            proof = self.tree.prove_inclusion(self.chain[i].height + 1, len(self.chain))
            first_state = self.tree.get_leaf(self.chain[i].height + 1)
            try:
                verify_inclusion(first_state, last_state, proof)
            except:
                return False
        return True
        
    def get_block(self, block_height: int) -> Block:
        """
        Retrieve a block from the blockchain at a specified height.
        
        Args:
            block_height (int): The height of the block to retrieve.
        
        Returns:
            Block: The block located at the specified height in the blockchain.
        """
        return self.chain[block_height]
    
    def check_every_transaction_of_a_block(self, block: Block) -> bool:
        """
        Check every transaction of a block for validity.
        
        Args:
            block (Block): The block to check transactions for.
        
        Returns:
            bool: True if all transactions in the block are valid, False otherwise.
        """
        if block.transactions[0] is None:
            return True
        if block.transactions[0].check_transaction_validity(self.coinbase_value) is False:
            return False
        for transaction in block.transactions[1:]:
            if transaction.check_transaction_validity() is False:
                return False
        return True
    
    def check_every_transaction_of_the_blockchain(self) -> bool:
        """
        Check every transaction of the entire blockchain for validity.
        
        Returns:
            bool: True if all transactions in the blockchain are valid, False otherwise.
        """
        for block in self.chain:
            if self.check_every_transaction_of_a_block(block) is False:
                return False
        return True
    
    def check_whole_blockchain(self) -> bool:
        """
        Check the integrity of the entire blockchain.

        This method performs multiple checks to ensure the integrity of the blockchain,
        including checking the consistency of the Merkle tree, verifying inclusion proofs,
        and validating every transaction in the blockchain.

        Returns:
            bool: True if the entire blockchain is valid, False otherwise.
        """
        if self.check_whole_blocks() is False:
            return False
        if self.check_consistency_tree() is False:
            return False
        if self.check_inclusion_tree() is False:
            return False
        if self.check_every_transaction_of_the_blockchain() is False:
            return False
        return True

    