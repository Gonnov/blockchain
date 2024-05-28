import unittest
from user.User import User
from transaction.Transaction import Transaction, TransactionOutput, TransactionInput


class testTransaction(unittest.TestCase):
    
    def test_get_transaction_serialized(self):
        first_user = User()
        second_user = User()
        transaction = Transaction(10, first_user.address, second_user.address, second_user.sign_transaction(b"Test transaction"))
        self.assertIsInstance(transaction.get_transaction_serialized(), bytes)
        
    def test_init_success(self):
        first_user = User()
        second_user = User()
        transaction = Transaction(10, first_user.address, second_user.address ,second_user.sign_transaction(b"Test transaction"))
        self.assertEqual(transaction.transaction_outputs.value, 10)
        self.assertEqual(transaction.transaction_outputs.receiver_address, first_user.address)
        self.assertEqual(transaction.transaction_inputs.transaction_output_hash, transaction.transaction_outputs.get_transaction_output_hash())
        self.assertEqual(transaction.transaction_inputs.output_index, 0)
        self.assertEqual(transaction.transaction_inputs.sequence_number, 0)
        self.assertTrue(transaction.check_transaction_validity())
        
        transaction = Transaction(10, second_user.address, first_user.address,first_user.sign_transaction(b"Test transaction"), 1, 1)
        self.assertEqual(transaction.transaction_outputs.value, 10)
        self.assertEqual(transaction.transaction_outputs.receiver_address, second_user.address)
        self.assertEqual(transaction.transaction_inputs.transaction_output_hash, transaction.transaction_outputs.get_transaction_output_hash())
        self.assertEqual(transaction.transaction_inputs.output_index, 1)
        self.assertEqual(transaction.transaction_inputs.sequence_number, 1)
    

class testTransactionOutput(unittest.TestCase):
    
    def test_get_transaction_output_hash(self):
        user = User()
        transaction_output = TransactionOutput(10, user.address)
        self.assertIsInstance(transaction_output.get_transaction_output_hash(), str)
        self.assertEqual(len(transaction_output.get_transaction_output_hash()), 64)
        
    def test_init(self):
        user = User()
        transaction_output = TransactionOutput(10, user.address)
        self.assertEqual(transaction_output.value, 10)
        self.assertEqual(transaction_output.receiver_address, user.address)
    
class testTransactionInput(unittest.TestCase):
    
    def test_init(self):
        user = User()
        transaction_output = TransactionOutput(10, user.address)
        transaction_input = TransactionInput(transaction_output, user.sign_transaction(b"Test transaction"), 0, 0)
        self.assertEqual(transaction_input.transaction_output_hash, transaction_output.get_transaction_output_hash())
        self.assertEqual(transaction_input.output_index, 0)
        self.assertEqual(transaction_input.sequence_number, 0)
        self.assertTrue(transaction_input.verify_signature(user.public_key.to_string(), b"Test transaction"))
        
        transaction_input = TransactionInput(transaction_output, user.sign_transaction(b"Test transaction"), 1, 1)
        self.assertEqual(transaction_input.transaction_output_hash, transaction_output.get_transaction_output_hash())
        self.assertEqual(transaction_input.output_index, 1)
        self.assertEqual(transaction_input.sequence_number, 1)
    
    def test_verify_signature(self):
        user = User()
        transaction_output = TransactionOutput(10, user.address)
        transaction_input = TransactionInput(transaction_output, user.sign_transaction(b"Test transaction"), 0, 0)
        self.assertTrue(transaction_input.verify_signature(user.public_key.to_string(), b"Test transaction"))
        self.assertFalse(transaction_input.verify_signature(user.public_key.to_string(), b"Test transaction1"))

    