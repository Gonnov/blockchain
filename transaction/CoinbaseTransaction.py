import pickle
import hashlib
import sys
import datetime as date
import uuid


class TransactionOutput:
    """
    Represents the output of a transaction.

    Attributes:
        amount (int): The amount to be transferred in the transaction.
        receiver_public_key (bytes): The public key of the receiver.

    Methods:
        get_transaction_output_hash(): Computes the hash of the transaction output.
    """

    def __init__(self, amount: int, miner_public_key: bytes) -> None:
        """
        Initialize the TransactionOutput.

        Args:
            amount (int): The amount to be transferred.
            miner_public_key (bytes): The public key of the receiver.
        """
        self.amount = amount
        if type(miner_public_key) == str:
            self.receiver_public_key = bytes.fromhex(miner_public_key)
        else:
            self.receiver_public_key = miner_public_key

    def get_transaction_output_hash(self) -> str:
        """
        Compute the hash of the transaction output.

        Returns:
            str: The SHA-256 hash of the serialized transaction output.
        """
        serialized_data = pickle.dumps(self)
        return hashlib.sha256(serialized_data).hexdigest()


class CoinbaseTransaction:
    """
    Represents a coinbase transaction.

    Attributes:
        transaction_outputs (TransactionOutput): The output of the coinbase transaction.
        transaction_id (uuid.UUID): The unique identifier of the transaction.
        timestamp (datetime.datetime): The timestamp when the transaction was created.

    Methods:
        get_transaction_serialized(): Serializes the transaction.
        check_transaction_validity(coinbase_value): Checks the validity of the transaction.
    """

    def __init__(self, amount: int, miner_public_key: bytes, extra_nonce) -> None:
        """
        Initialize the CoinbaseTransaction.

        Args:
            amount (int): The amount to be transferred.
            miner_public_key (bytes): The public key of the miner.
        """
        self.transaction_outputs = TransactionOutput(amount, miner_public_key)
        self.transaction_id = uuid.uuid4()
        self.timestamp = date.datetime.now()
        self.extra_nonce = extra_nonce

    def get_transaction_serialized(self) -> bytes:
        """
        Serialize the transaction.

        Returns:
            bytes: The serialized transaction as a byte stream.
        """
        return pickle.dumps(self)

    def check_transaction_validity(self, coinbase_value: int) -> bool:
        """
        Check the validity of the transaction.

        Args:
            coinbase_value (int): The maximum allowable value for the coinbase transaction.

        Returns:
            bool: True if the transaction is valid, False otherwise.
        """
        if sys.getsizeof(self) > 4194304:  # 4MB
            return False
        if self.transaction_outputs.amount > coinbase_value:
            return False
        if self.transaction_outputs.amount < 0:
            return False
        return True
