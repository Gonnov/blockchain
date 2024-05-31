import unittest
import ecdsa
from user.User import User
from transaction.TransactionData import TransactionData

class TestUser(unittest.TestCase):
    def test_generate_address(self):
        user = User()
        address = user.generate_address()
        self.assertIsInstance(address, str)
        self.assertEqual(len(address), 40)  # Check if the address is 40 characters long
    
    def test_sign_transaction(self):
        user = User()
        user2 = User()
        transactionData = TransactionData(user.public_key, user2.public_key, 10)
        signature = user.sign_transaction(transactionData.serialize())
        self.assertTrue(ecdsa.VerifyingKey.from_string(user.public_key).verify(signature, transactionData.serialize()))