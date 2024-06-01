import pickle
import hashlib
import sys
import datetime as date
import uuid

class TransactionOutput:
    def __init__(self, amount: int, miner_public_key: bytes) -> None:
        self.amount = amount
        self.receiver_public_key = miner_public_key
        
    def get_transaction_output_hash(self) -> str:
        serialized_data = pickle.dumps(self)
        return hashlib.sha256(serialized_data).hexdigest()


class CoinbaseTransaction:
    def __init__(self, amount: int, miner_public_key: bytes) -> None:
        self.transaction_outputs = TransactionOutput(amount, miner_public_key)
        self.transaction_id = uuid.uuid4()
        self.timestamp = date.datetime.now()
        
    def get_transaction_serialized(self) -> bytes:
        return pickle.dumps(self)
    
    def check_transaction_validity(self, coinbase_value: int) -> bool:
        if sys.getsizeof(self) > 4194304: # 4MB
            return False
        if self.transaction_outputs.amount > coinbase_value:
            return False
        if self.transaction_outputs.amount < 0:
            return False
        return True