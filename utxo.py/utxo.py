class Utxo:
    def __init__(self, transaction_output_hash: str, receiver_address: str, value: int) -> None:
        self.transaction_output_hash = transaction_output_hash
        self.receiver_address = receiver_address
        self.value = value