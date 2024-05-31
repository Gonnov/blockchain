import unittest
from user.User import User
from transaction.Transaction import Transaction, TransactionOutput, TransactionInput
from transaction.TransactionData import TransactionData
import time
import pickle

class testTransaction(unittest.TestCase):
    
    def test_get_transaction_serialized(self):
        first_user = User()
        second_user = User()
        transactionData = TransactionData(first_user.public_key, second_user.public_key, 10)
        sender_signature = first_user.sign_transaction(transactionData.serialize())
        transaction = Transaction(transactionData, sender_signature)
        self.assertIsInstance(transaction.get_transaction_serialized(), bytes)
        
    def test_init_success(self):
        first_user = User()
        second_user = User()
        transactionData = TransactionData(second_user.public_key, first_user.public_key ,10)
        sender_signature = second_user.sign_transaction(transactionData.serialize())
        transaction = Transaction(transactionData, sender_signature)
        self.assertEqual(transaction.transaction_outputs.amount, 10)
        self.assertEqual(transaction.transaction_outputs.receiver_public_key, first_user.public_key)
        self.assertEqual(transaction.transaction_inputs.transaction_output_hash, \
            transaction.transaction_outputs.get_transaction_output_hash())
        self.assertEqual(transaction.transaction_inputs.output_index, 0)
        self.assertEqual(transaction.transaction_inputs.sequence_number, 0)
        self.assertTrue(transaction.check_transaction_validity())
    

class testTransactionOutput(unittest.TestCase):
    
    def test_get_transaction_output_hash(self):
        user = User()
        transaction_output = TransactionOutput(10, user.public_key)
        self.assertIsInstance(transaction_output.get_transaction_output_hash(), str)
        self.assertEqual(len(transaction_output.get_transaction_output_hash()), 64)
        
    def test_init(self):
        user = User()
        transaction_output = TransactionOutput(10, user.public_key)
        self.assertEqual(transaction_output.amount, 10)
        self.assertEqual(transaction_output.receiver_public_key, user.public_key)
    
class testTransactionInput(unittest.TestCase):
    
    def test_init(self):
        user = User()
        user2 = User()
        transaction_output = TransactionOutput(10, user.address)
        transactionData = TransactionData(user.public_key, user2.public_key, 10)
        transaction_input = TransactionInput(transaction_output, user.public_key, user.sign_transaction(transactionData.serialize()), 0, 0)
        self.assertEqual(transaction_input.transaction_output_hash, transaction_output.get_transaction_output_hash())
        self.assertEqual(transaction_input.output_index, 0)
        self.assertEqual(transaction_input.sequence_number, 0)
        # self.assertTrue(transaction_input.verify_signature(user.public_key.to_string(), b"Test transaction"))
        transaction_input = TransactionInput(transaction_output, user.public_key, user.sign_transaction(b"Test transaction"), 1, 1)
        self.assertEqual(transaction_input.transaction_output_hash, transaction_output.get_transaction_output_hash())
        self.assertEqual(transaction_input.output_index, 1)
        self.assertEqual(transaction_input.sequence_number, 1)
    
    def test_verify_signature(self):
        user = User()
        user2 = User()
        transaction_output = TransactionOutput(10, user.address)
        transactionData = TransactionData(user.public_key, user2.public_key, 10)
        falseTransactionData = TransactionData(user.public_key, user2.public_key, 12)
        transaction_input = TransactionInput(transaction_output, user.public_key, user.sign_transaction(transactionData.serialize()), 0, 0)
        self.assertTrue(transaction_input.verify_signature(transactionData))
        self.assertFalse(transaction_input.verify_signature(falseTransactionData))

    