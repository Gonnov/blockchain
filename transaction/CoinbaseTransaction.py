import pickle
import hashlib
import sys
import datetime as date

class TransactionOutput:
    def __init__(self, value: int, miner_address: str) -> None:
        self.value = value
        self.receiver_address = miner_address
        
    def get_transaction_output_hash(self) -> str:
        serialized_data = pickle.dumps(self)
        return hashlib.sha256(serialized_data).hexdigest()


class CoinbaseTransaction:
    def __init__(self, value: int, miner_address: str, extra_nonce) -> None:
        self.transaction_outputs = TransactionOutput(value, miner_address)
        self.timestamp = date.datetime.now()
        self.extra_nonce = extra_nonce
        
    def get_transaction_serialized(self) -> bytes:
        return pickle.dumps(self)
    
    def check_transaction_validity(self) -> bool:
        if sys.getsizeof(self) > 4194304: # 4MB
            return False
        if self.transaction_outputs.value < 0 or self.transaction_outputs.value > 21000000:
            return False
        return True