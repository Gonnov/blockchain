import hashlib
import ecdsa


class Wallet:
    """
    Represents a digital wallet using elliptic curve cryptography.

    Attributes:
        private_key (ecdsa.SigningKey): The private key for signing transactions.
        public_key (bytes): The public key corresponding to the private key.
        address (str): The generated address for the wallet.

    Methods:
        generate_address(): Generates a wallet address from the public key.
        sign_transaction(transactionData): Signs the given transaction data.
    """

    def __init__(self):
        """
        Initialize the Wallet.

        Generates a new elliptic curve key pair and creates a wallet address.
        """
        self.private_key = ecdsa.SigningKey.generate()
        self.public_key = self.private_key.get_verifying_key().to_string()
        self.address = self.generate_address()

    def generate_address(self) -> str:
        """
        Generate a wallet address from the public key.

        This method first computes the SHA-256 hash of the public key and then computes
        the RIPEMD-160 hash of the SHA-256 hash to create the wallet address.

        Returns:
            str: The wallet address as a hexadecimal string.
        """
        public_key_bytes = self.public_key
        address_bytes = hashlib.sha256(public_key_bytes).digest()
        return hashlib.new('ripemd160', address_bytes).hexdigest()

    def sign_transaction(self, transactionData: bytes) -> bytes:
        """
        Sign the given transaction data with the wallet's private key.

        Args:
            transactionData (bytes): The transaction data to sign.

        Returns:
            bytes: The signature of the transaction data.
        """
        return self.private_key.sign(transactionData)
