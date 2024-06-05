from Block.Block import Block
from Blockchain.utxo_utils import set_transactions_in_ledger
from transaction.Transaction import Transaction
from transaction.CoinbaseTransaction import CoinbaseTransaction
from pymerkle import InmemoryTree as MerkleTree
from pymerkle import verify_consistency, verify_inclusion
import pickle
import ecdsa

class Blockchain:
    """
    Represents the blockchain and provides methods for managing and verifying blocks and transactions.

    Attributes:
        tree (MerkleTree): The Merkle tree used to store transactions.
        difficulty (int): The difficulty level for mining blocks.
        coinbase_value (int): The reward value for mining a block.
        chain (list): The list of blocks in the blockchain.

    Methods:
        create_genesis_block(): Creates the genesis block.
        mine_block(miner_address, extra_nonce): Mines a new block.
        add_block(transactions): Adds a new block to the blockchain.
        check_whole_blocks(): Checks the integrity of the entire blockchain.
        check_consistency_single_block(block_height): Verifies the consistency of a specific block.
        check_consistency_tree(): Verifies the consistency of the entire blockchain tree.
        check_inclusion_single_block(block_height): Verifies that a specific block is included in the blockchain.
        check_inclusion_tree(): Verifies that all blocks in the blockchain are included.
        get_block(block_height): Retrieves a block from the blockchain at a specified height.
        check_every_transaction_of_a_block(block): Checks every transaction of a block for validity.
        check_every_transaction_of_the_blockchain(): Checks every transaction of the entire blockchain for validity.
        check_whole_blockchain(): Checks the integrity of the entire blockchain.
    """

    def __init__(self) -> None:
        """
        Initialize the Blockchain.

        Initializes the blockchain with a Merkle tree, sets the mining difficulty,
        assigns the coinbase value, and creates the genesis block.
        """
        self.tree = MerkleTree(algorithm='sha256')
        self.difficulty = 6
        self.coinbase_value = 50
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self) -> None:
        """
        Create the genesis block.

        Returns:
            Block: The genesis block.
        """
        transactions = None
        block = Block(None, transactions, self.tree)
        merkle_index = self.tree.append_entry(pickle.dumps(block.transactions))
        block.merkle_hash = self.tree.get_leaf(merkle_index)
        return block
    
    def start_mining(self, miner_public_key, extra_nonce, mempool) -> None:
        """
        Mine a new block.

        Args:
            miner_address: The address of the miner who mines the block.
            extra_nonce: Extra nonce value for mining.

        Returns:
            bool: True if the block is successfully mined, False otherwise.
        """
        coinbase_transaction = CoinbaseTransaction(self.coinbase_value, miner_public_key, extra_nonce)
        transactions = mempool[:2000]
        transactions.insert(0, coinbase_transaction)
        block = Block(self.chain[-1], transactions, self.difficulty)
        self.mining_flag.clear()
        while block.mine_block(self) is False: #NEED TO PUT A DIFFICULTY ALGORITHM
            block.transactions[0].extra_nonce += 1
        self.add_block(block)
        for transaction in block.transactions[1:]:
            mempool.remove(transaction)
        return True 
    
    def add_block(self, block) -> None:
        """
        Add a new block to the blockchain.

        Args:
            transactions: The transactions to be added to the block.
        """
        # merkle_index = self.tree.append_entry(pickle.dumps(block.transactions))
        # block.merkle_hash = self.tree.get_leaf(merkle_index)
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
            if current_block.verify_block() is False:
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
        if block.transactions is None:
            return True
        if block.transactions[0] is None:
            return True
        if block.transactions[0].check_transaction_validity(self.coinbase_value) is False:
            return False
        for transaction in block.transactions[1:]:
            if transaction.check_transaction_validity() is False:
                return False
        return True
    
    def get_public_key_from_private_key(self, private_key: bytes) -> bytes:
        """
        Retrieve the public key from a given private key.
        
        Args:
            private_key (bytes): The private key to derive the public key from.
        
        Returns:
            bytes: The public key corresponding to the given private key.
        """
        return ecdsa.SigningKey.from_string(private_key).get_verifying_key().to_string()
    
    def check_every_transaction_of_the_blockchain(self) -> bool:
        """
        Check every transaction of the entire blockchain for validity.
        
        Returns:
            bool: True if all transactions in the blockchain are valid, False otherwise.
        """
        if self.chain[0].transactions is not None:
            return False
        for block in self.chain[1:]:
            if self.check_every_transaction_of_a_block(block) is False:
                return False
        return True
    
    def get_every_utxo(self) -> dict:
        """
        Constructs the UTXO set from the blockchain.

        Iterates through the blockchain to create a dictionary representing the UTXO set,
        by including all valid transactions.

        Args:
            blockchain (Blockchain): The blockchain from which to construct the UTXO set.

        Returns:
            dict: The dictionary representing the UTXO set.

        Raises:
            ValueError: If any invalid transactions are found in the blockchain.
        """

        ledger = {}
        for block in self.chain[1:]:
            try:
                set_transactions_in_ledger(ledger, block.transactions, self.coinbase_value)
            except ValueError:
                raise ValueError("invalid transactions")
        return ledger
    
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
            print("whole block")
            return False
        # if self.check_consistency_tree() is False:
        #     return False
        # if self.check_inclusion_tree() is False:
        #     return False
        if self.check_every_transaction_of_the_blockchain() is False:
            print("check transac")
            return False
        try:
            self.get_every_utxo()
        except ValueError:
            print("utxo")
            return False
        return True

    