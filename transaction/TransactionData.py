import uuid
import datetime as date
import pickle

class TransactionData:
    def __init__(self, sender_public_key: str, receiver_public_key: str, \
        transaction_amount: int, transaction_timestamp=None, transaction_id=None) -> None:
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.transaction_amount= transaction_amount
        if transaction_timestamp is None:
            self.transaction_timestamp = date.datetime.now().timestamp()
        else:
            self.transaction_timestamp = transaction_timestamp
        if transaction_id is None:
            self.transaction_id = uuid.uuid4()
        else:
            self.transaction_id = transaction_id
        
    def serialize(self) -> bytes:
        return pickle.dumps(self)
    