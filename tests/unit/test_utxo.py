from Utxo.Utxo import Utxo
from Blockchain.Blockchain import Blockchain
from user.Wallet import Wallet
from transaction.TransactionData import TransactionData
from transaction.Transaction import Transaction
from tests.unit.utils import setup_blockchain_n_blocks
import unittest



class TestBlockchain(unittest.TestCase):
    def test_utxo_2_blocks(self):
        blockchain = setup_blockchain_n_blocks(2)
        self.assertTrue(len(blockchain.chain) == 2)
        utxo = Utxo(blockchain)
        self.assertTrue(len(utxo.ledger) == 3)
        values = utxo.ledger.values()
        for value in values:
            self.assertTrue(value >= 16.666666)
            self.assertTrue(value <= 16.666667)
            
    def test_utxo_10_blocks(self):
        blockchain = setup_blockchain_n_blocks(10)
        self.assertTrue(len(blockchain.chain) == 10)
        utxo = Utxo(blockchain)
        self.assertTrue(len(utxo.ledger) == 3)
        values = utxo.ledger.values()
        for value in values:
            self.assertTrue(value >= 150)
            self.assertTrue(value <= 150.00001)
            
    def test_utxo_100_blocks(self):
        blockchain = setup_blockchain_n_blocks(100)
        self.assertTrue(len(blockchain.chain) == 100)
        utxo = Utxo(blockchain)
        self.assertTrue(len(utxo.ledger) == 3)
        values = utxo.ledger.values()
        for value in values:
            self.assertTrue(value >= 1649.99999)
            self.assertTrue(value <= 1650.00001)
            
    def test_utxo_no_transactions_in_block(self):
        blockchain = Blockchain()
        utxo = Utxo(blockchain)
        self.assertTrue(len(utxo.ledger) == 0)    
    