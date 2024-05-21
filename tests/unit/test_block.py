import unittest
import ecdsa
from block.Block import Block
from pymerkle import InmemoryTree as MerkleTree

class TestBlock(unittest.TestCase):
    
    def test_calculate_hash(self):
        tree = MerkleTree()
        block = Block(None, ["4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"], tree)
        self.assertIsInstance(block.calculate_hash(), str)
        self.assertEqual(len(block.calculate_hash()), 64)
        
    def test_init(self):
        tree = MerkleTree()
        block = Block(None, ["4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"], tree)
        self.assertEqual(block.height, 0)
        self.assertEqual(block.previous_hash, None)
        self.assertEqual(block.height + 1, 1)
        self.assertEqual(block.transactions, ["4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"])
        
        second_block = Block(block, ["4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"], tree)
        self.assertEqual(second_block.height, 1)
        self.assertEqual(second_block.previous_hash, block.calculate_hash())
        self.assertEqual(second_block.height + 1, 2)
        self.assertEqual(second_block.transactions, ["4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"])
        
        
    