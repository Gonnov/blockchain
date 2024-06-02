from Blockchain.Blockchain import Blockchain
from tests.unit.utils import setup_blockchain_n_blocks
import unittest



class TestBlockchain(unittest.TestCase):
    def test_utxo_2_blocks(self):
        blockchain = setup_blockchain_n_blocks(2)
        self.assertTrue(len(blockchain.chain) == 2)
        utxo = blockchain.get_every_utxo()
        self.assertTrue(len(utxo) == 3)
        values = utxo.values()
        for value in values:
            self.assertTrue(value >= 16.666666)
            self.assertTrue(value <= 16.666667)
        blockchain.check_whole_blockchain()
            
    def test_utxo_10_blocks(self):
        blockchain = setup_blockchain_n_blocks(10)
        self.assertTrue(len(blockchain.chain) == 10)
        utxo = blockchain.get_every_utxo()
        self.assertTrue(len(utxo) == 3)
        values = utxo.values()
        for value in values:
            self.assertTrue(value >= 150)
            self.assertTrue(value <= 150.00001)
        blockchain.check_whole_blockchain()
            
    def test_utxo_100_blocks(self):
        blockchain = setup_blockchain_n_blocks(100)
        self.assertTrue(len(blockchain.chain) == 100)
        utxo = blockchain.get_every_utxo()
        self.assertTrue(len(utxo) == 3)
        values = utxo.values()
        for value in values:
            self.assertTrue(value >= 1649.99999)
            self.assertTrue(value <= 1650.00001)
        blockchain.check_whole_blockchain()
            
    