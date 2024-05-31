import pickle
import hashlib
import ecdsa
import sys
import datetime as date
from transaction.TransactionData import TransactionData

class TransactionOutput:
    def __init__(self, amount: int, receiver_public_key: bytes) -> None:
        self.amount = amount
        self.receiver_public_key = receiver_public_key
        
    def get_transaction_output_hash(self) -> str:
        serialized_data = pickle.dumps(self)
        return hashlib.sha256(serialized_data).hexdigest()

class TransactionInput:
    def __init__(self, transaction_output: TransactionOutput, sender_public_key: bytes, sender_signature, 
                 output_index: int, sequence_number: int) -> None:
        self.transaction_output_hash = transaction_output.get_transaction_output_hash()
        self.sender_public_key = sender_public_key
        self.output_index = output_index
        self.sender_signature = sender_signature
        self.sequence_number = sequence_number
        
    def verify_signature(self, transactionData) -> bool:
        vk = ecdsa.VerifyingKey.from_string(self.sender_public_key)
        try:
            return vk.verify(self.sender_signature, transactionData.serialize())
        except ecdsa.BadSignatureError:
            return False

class Transaction:
    def __init__(self, transactionData: TransactionData, sender_signature: str, 
                 output_index: int=0, sequence_number: int=0) -> None:
        self.transaction_outputs = TransactionOutput(\
                transactionData.transaction_amount, transactionData.receiver_public_key)
        self.transaction_inputs = TransactionInput(self.transaction_outputs, transactionData.sender_public_key, \
                sender_signature, output_index, sequence_number)
        self.transaction_timestamp = transactionData.transaction_timestamp
        self.transaction_id = transactionData.transaction_id
        
    def get_transaction_serialized(self) -> bytes:
        return pickle.dumps(self)
    
    def check_transaction_validity(self) -> bool:
        transactionData = TransactionData(self.transaction_inputs.sender_public_key, \
            self.transaction_outputs.receiver_public_key, self.transaction_outputs.amount, \
                self.transaction_timestamp, self.transaction_id)
        if sys.getsizeof(self) > 4194304: # 4MB
            return False
        if self.transaction_inputs.sender_public_key == self.transaction_outputs.receiver_public_key:
            return False
        if self.transaction_inputs.verify_signature(transactionData) is False:
            return False
        if self.transaction_outputs.amount <= 0:
            return False
        if self.transaction_inputs.sequence_number < 0 \
         or self.transaction_inputs.sequence_number > 2147483647:
            return False
        if self.transaction_inputs.output_index < 0:
            return False
        return True
    