import hashlib
import ecdsa


class User:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate()
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
        public_key_bytes = self.public_key.to_string()
        address_bytes = hashlib.sha256(public_key_bytes).digest()
        return hashlib.new('ripemd160', address_bytes).hexdigest()

    def sign_transaction(self, transaction):
        return self.private_key.sign(transaction)