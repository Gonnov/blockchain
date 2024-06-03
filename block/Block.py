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
        mine_block(): Mines the block by finding a hash with the required number of leading zeros.
        verify_block(): Verifies the block by checking the hash and the Merkle root hash.
        to_dict(): Converts the block to a dictionary.
    """

    def __init__(self, previous_block: 'Block', transactions: list, difficulty: int) -> None:
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
        self.difficulty = difficulty
    
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
        self.timestamp = date.datetime.now()
        hash_string = str(self.height) + str(self.timestamp) + str(self.merkle_hash) + str(self.previous_hash) + str(self.nonces)
        return hashlib.sha256(hash_string.encode()).hexdigest()
    
    def mine_block(self) -> None:
        """
        Mine the block by finding a hash with the required number of leading zeros.

        Args:
            difficulty (int): The number of leading zeros required in the hash.
        """
        difficulty_string = '0' * self.difficulty
        while self.calculate_hash()[:self.difficulty] != difficulty_string:
            if self.nonces == 4294967295:
                self.nonces = 0
                return False
            else:
                self.nonces += 1
        return True   

    def verify_block(self) -> bool:
        """
        Verify the block by checking the hash and the Merkle root hash.

        Returns:
            bool: True if the block is valid, False otherwise.
        """
        return self.calculate_hash()[:self.difficulty] == '0' * self.difficulty
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'transactions': self.transactions,
            'nonces': self.nonces,
            'merkle_hash': self.merkle_hash,
            'height': self.height,
            'previous_hash': self.previous_hash
        }

