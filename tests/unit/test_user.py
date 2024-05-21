import unittest
import ecdsa
from user.User import User

class TestUser(unittest.TestCase):
    def test_generate_address(self):
        user = User()
        address = user.generate_address()
        self.assertIsInstance(address, str)
        self.assertEqual(len(address), 40)  # Check if the address is 40 characters long
    
    def test_sign_transaction(self):
        user = User()
        message = b"Test transaction"
        signature = user.sign_transaction(message)
        self.assertTrue(ecdsa.VerifyingKey.from_string(user.public_key.to_string()).verify(signature, message))