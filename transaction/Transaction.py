import pickle
import hashlib
import ecdsa
import sys
import datetime as date
from transaction.TransactionData import TransactionData

class TransactionOutput:
    """
    Represents the output of a transaction.

    Attributes:
        amount (int): The amount to be transferred in the transaction.
        receiver_public_key (bytes): The public key of the receiver.

    Methods:
        get_transaction_output_hash(): Computes the hash of the transaction output.
    """

    def __init__(self, amount: int, receiver_public_key: bytes) -> None:
        """
        Initialize the TransactionOutput.

        Args:
            amount (int): The amount to be transferred.
            receiver_public_key (bytes): The public key of the receiver.
        """
        self.amount = amount
        if type(receiver_public_key) == str:
            self.receiver_public_key = bytes.fromhex(receiver_public_key)
        else:
            self.receiver_public_key = receiver_public_key

    def get_transaction_output_hash(self) -> str:
        """
        Compute the hash of the transaction output.

        Returns:
            str: The SHA-256 hash of the serialized transaction output.
        """
        serialized_data = pickle.dumps(self)
        return hashlib.sha256(serialized_data).hexdigest()


class TransactionInput:
    """
    Represents the input of a transaction.

    Attributes:
        transaction_output_hash (str): The hash of the transaction output.
        sender_public_key (bytes): The public key of the sender.
        sender_signature (bytes): The signature of the sender.
        output_index (int): The index of the output.
        sequence_number (int): The sequence number of the transaction.

    Methods:
        verify_signature(transactionData): Verifies the sender's signature.
    """

    def __init__(self, transaction_output: TransactionOutput, sender_public_key: bytes, sender_signature: bytes, 
                 output_index: int, sequence_number: int) -> None:
        """
        Initialize the TransactionInput.

        Args:
            transaction_output (TransactionOutput): The transaction output.
            sender_public_key (bytes): The public key of the sender.
            sender_signature (bytes): The signature of the sender.
            output_index (int): The index of the output.
            sequence_number (int): The sequence number of the transaction.
        """
        self.transaction_output_hash = transaction_output.get_transaction_output_hash()
        if type(sender_public_key) == str:
            sender_public_key = bytes.fromhex(sender_public_key)
        else:
            sender_public_key = sender_public_key
        self.sender_signature = sender_signature
        self.output_index = output_index
        self.sequence_number = sequence_number

    def verify_signature(self, transactionData: TransactionData) -> bool:
        """
        Verify the sender's signature.

        Args:
            transactionData (TransactionData): The data of the transaction.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        vk = ecdsa.VerifyingKey.from_string(self.sender_public_key)
        try:
            return vk.verify(self.sender_signature, transactionData.serialize())
        except ecdsa.BadSignatureError:
            return False


class Transaction:
    """
    Represents a transaction.

    Attributes:
        transaction_outputs (TransactionOutput): The outputs of the transaction.
        transaction_inputs (TransactionInput): The inputs of the transaction.
        transaction_timestamp (datetime): The timestamp of the transaction.
        transaction_id (str): The unique identifier of the transaction.

    Methods:
        get_transaction_serialized(): Serializes the transaction.
        check_transaction_validity(): Checks the validity of the transaction.
    """

    def __init__(self, transactionData: TransactionData, sender_signature: str, 
                 output_index: int = 0, sequence_number: int = 0) -> None:
        """
        Initialize the Transaction.

        Args:
            transactionData (TransactionData): The data of the transaction.
            sender_signature (str): The signature of the sender.
            output_index (int, optional): The index of the output. Defaults to 0.
            sequence_number (int, optional): The sequence number of the transaction. Defaults to 0.
        """
        self.transaction_outputs = TransactionOutput(transactionData.transaction_amount, 
                                                     transactionData.receiver_public_key)
        self.transaction_inputs = TransactionInput(self.transaction_outputs, 
                                                   transactionData.sender_public_key, 
                                                   sender_signature, 
                                                   output_index, 
                                                   sequence_number)
        self.transaction_timestamp = transactionData.transaction_timestamp
        self.transaction_id = transactionData.transaction_id

    def get_transaction_serialized(self) -> bytes:
        """
        Serialize the transaction.

        Returns:
            bytes: The serialized transaction as a byte stream.
        """
        return pickle.dumps(self)

    def check_transaction_validity(self) -> bool:
        """
        Check the validity of the transaction.

        Returns:
            bool: True if the transaction is valid, False otherwise.
        """
        transactionData = TransactionData(self.transaction_inputs.sender_public_key, 
                                          self.transaction_outputs.receiver_public_key, 
                                          self.transaction_outputs.amount, 
                                          self.transaction_timestamp, 
                                          self.transaction_id)
        if sys.getsizeof(self) > 4194304:  # 4MB
            return False
        if self.transaction_inputs.sender_public_key == self.transaction_outputs.receiver_public_key:
            return False
        if not self.transaction_inputs.verify_signature(transactionData):
            return False
        if self.transaction_outputs.amount <= 0:
            return False
        if self.transaction_inputs.sequence_number < 0 or self.transaction_inputs.sequence_number > 2147483647:
            return False
        if self.transaction_inputs.output_index < 0:
            return False
        return True
