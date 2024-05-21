import pickle
import hashlib
import ecdsa
import sys
import datetime as date

class TransactionOutput:
    def __init__(self, value: int, receiver_address: str) -> None:
        self.value = value
        self.receiver_address = receiver_address
        
    def get_transaction_output_hash(self) -> str:
        serialized_data = pickle.dumps(self)
        return hashlib.sha256(serialized_data).hexdigest()

class TransactionInput:
    def __init__(self, transaction_output: TransactionOutput, sender_signature :str, 
                 output_index: int, sequence_number: int) -> None:
        self.transaction_output_hash = transaction_output.get_transaction_output_hash()
        self.output_index = output_index
        self.sender_signature = sender_signature
        self.sequence_number = sequence_number
        
    def verify_signature(self, sender_public_key: str, message) -> bool:
        vk = ecdsa.VerifyingKey.from_string(sender_public_key)
        try:
            return vk.verify(self.sender_signature, message)
        except ecdsa.BadSignatureError:
            return False

class Transaction:
    def __init__(self, value: int, receiver_address: str, sender_signature: str, 
                 output_index: int=0, sequence_number: int=0) -> None:
        self.transaction_outputs = TransactionOutput(value, receiver_address)
        self.transaction_inputs = TransactionInput(self.transaction_outputs, \
                sender_signature, output_index, sequence_number)
        self.timestamp = date.datetime.now()
        
    def get_transaction_serialized(self) -> bytes:
        return pickle.dumps(self)
    
    def check_transaction_validity(self) -> bool:
        if sys.getsizeof(self) > 4194304: # 4MB
            return False
        if self.transaction_outputs.value < 0 or self.transaction_outputs.value > 21000000:
            return False
        if self.transaction_inputs.sequence_number < 0 \
         or self.transaction_inputs.sequence_number > 2147483647:
            return False
        if self.transaction_inputs.output_index < 0:
            return False
        return True
    