import pickle
import datetime as date
import uuid

class TransactionData:
    """
    Represents the data of a transaction.

    Attributes:
        sender_public_key (str): The public key of the sender.
        receiver_public_key (str): The public key of the receiver.
        transaction_amount (int): The amount of the transaction.
        transaction_timestamp (float): The timestamp of the transaction.
        transaction_id (uuid.UUID): The unique identifier of the transaction.

    Methods:
        serialize(): Serializes the transaction data.
    """

    def __init__(self, sender_public_key: str, receiver_public_key: str, 
                 transaction_amount: int, transaction_timestamp=None, transaction_id=None) -> None:
        """
        Initialize the TransactionData.

        Args:
            sender_public_key (str): The public key of the sender.
            receiver_public_key (str): The public key of the receiver.
            transaction_amount (int): The amount of the transaction.
            transaction_timestamp (float, optional): The timestamp of the transaction. Defaults to None.
            transaction_id (uuid.UUID, optional): The unique identifier of the transaction. Defaults to None.
        """
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.transaction_amount = transaction_amount
        if transaction_timestamp is None:
            self.transaction_timestamp = date.datetime.now().timestamp()
        else:
            self.transaction_timestamp = transaction_timestamp
        if transaction_id is None:
            self.transaction_id = uuid.uuid4()
        else:
            self.transaction_id = transaction_id
        
    def serialize(self) -> bytes:
        """
        Serialize the transaction data.

        Returns:
            bytes: The serialized transaction data.
        """
        return pickle.dumps(self)
