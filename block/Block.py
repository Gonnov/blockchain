import hashlib
import datetime as date
from pymerkle import InmemoryTree as MerkleTree

class Block:
    """
    Represents a block in the blockchain.

    Attributes:
        timestamp (datetime): The timestamp when the block was created.
        transactions (list): The list of transactions included in the block.
        nonces (int): The nonce value used in mining the block.
        merkle_hash (str): The Merkle root hash of the transactions in the block.
        height (int): The height of the block in the blockchain.
        previous_hash (str): The hash of the previous block in the blockchain.

    Methods:
        calculate_hash(): Calculates the hash of the block.
    """

    def __init__(self, previous_block: 'Block', transactions: list, tree: MerkleTree) -> None:
        """
        Initialize a new block.

        Args:
            previous_block (Block): The previous block in the blockchain.
            transactions (list): The list of transactions to be included in the block.
            tree (MerkleTree): The Merkle tree used to compute the Merkle root.

        Attributes:
            timestamp (datetime): The timestamp when the block was created.
            transactions (list): The list of transactions included in the block.
            nonces (int): The nonce value used in mining the block.
            merkle_hash (str): The Merkle root hash of the transactions in the block.
            height (int): The height of the block in the blockchain.
            previous_hash (str): The hash of the previous block in the blockchain.
        """
        self.timestamp = date.datetime.now()
        self.transactions = transactions
        self.nonces = 0
        self.merkle_hash = None
    
        if previous_block is None:
            self.height = 0
            self.previous_hash = None
        else:
            self.height = previous_block.height + 1
            self.previous_hash = previous_block.calculate_hash()
        
    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block.

        Combines the block's height, timestamp, Merkle root hash, and previous block's hash
        to compute a SHA-256 hash of the block.

        Returns:
            str: The SHA-256 hash of the block.
        """
        hash_string = str(self.height) + str(self.timestamp) + str(self.merkle_hash) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()


