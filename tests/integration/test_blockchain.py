import unittest
from Blockchain.Blockchain import Blockchain
from tests.unit.utils import make_basic_transaction, make_basic_coinbase_transaction
from user.Wallet import Wallet
import random, string

class TestBlockchain(unittest.TestCase):
    def test_blockchain_one_block_no_mining_success(self):
        blockchain = Blockchain()
        
        #genesis block test
        self.assertEqual(len(blockchain.chain), 1)
        self.assertEqual(blockchain.chain[0].previous_hash, None)
        
        #add block test
        first_transaction = make_basic_transaction()
        second_transaction = make_basic_transaction()
        thrid_transaction = make_basic_transaction()
        blockchain.add_block([first_transaction, second_transaction, thrid_transaction])
        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(blockchain.check_whole_blocks(), True)
        self.assertEqual(blockchain.chain[1].previous_hash, blockchain.chain[0].calculate_hash())
        self.assertEqual(blockchain.chain[1].height, 1)
        
        #merkle tree test
        blockchain.check_inclusion_tree()
        blockchain.check_inclusion_single_block(0)
        blockchain.check_inclusion_single_block(1)
        blockchain.check_consistency_tree()
        blockchain.check_consistency_single_block(0)
        blockchain.check_consistency_single_block(1)
        
    def test_blockchain_two_blocks_no_mmining_success(self):
        blockchain = Blockchain()
        
        #add block test
        coinbase_transaction = make_basic_coinbase_transaction(blockchain.coinbase_value)
        first_transaction = make_basic_transaction()
        second_transaction = make_basic_transaction()
        thrid_transaction = make_basic_transaction()
        blockchain.add_block([coinbase_transaction, first_transaction, second_transaction, thrid_transaction])
        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(blockchain.check_whole_blocks(), True)
        self.assertEqual(blockchain.chain[1].previous_hash, blockchain.chain[0].calculate_hash())
        self.assertEqual(blockchain.chain[1].height, 1)
        
        #add block test
        coinbase_transaction = make_basic_coinbase_transaction(blockchain.coinbase_value)
        first_transaction = make_basic_transaction()
        second_transaction = make_basic_transaction()
        thrid_transaction = make_basic_transaction()
        blockchain.add_block([coinbase_transaction, first_transaction, second_transaction, thrid_transaction])
        self.assertEqual(len(blockchain.chain), 3)
        self.assertEqual(blockchain.check_whole_blocks(), True)
        self.assertEqual(blockchain.chain[2].previous_hash, blockchain.chain[1].calculate_hash())
        self.assertEqual(blockchain.chain[2].height, 2)
                
        #merkle tree test
        blockchain.check_inclusion_tree()
        blockchain.check_inclusion_single_block(0)
        blockchain.check_inclusion_single_block(1)
        blockchain.check_inclusion_single_block(2)
        blockchain.check_consistency_tree()
        blockchain.check_consistency_single_block(0)
        blockchain.check_consistency_single_block(1)
        blockchain.check_consistency_single_block(2)

    def test_mining_no_transaction_success(self):
        blockchain = Blockchain()
        miner = Wallet()
        #mine block test
        extra_nonce = 'xzOFl8XXAP4vytPn'
        while blockchain.mine_block(miner.public_key, extra_nonce) is False:
            extra_nonce =''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(blockchain.check_whole_blocks(), True)
        self.assertEqual(blockchain.chain[1].previous_hash, blockchain.chain[0].calculate_hash())
        self.assertEqual(blockchain.chain[1].height, 1)
        
        #merkle tree test
        blockchain.check_inclusion_tree()
        blockchain.check_inclusion_single_block(0)
        blockchain.check_inclusion_single_block(1)
        blockchain.check_consistency_tree()
        blockchain.check_consistency_single_block(0)
        blockchain.check_consistency_single_block(1)
                      
   