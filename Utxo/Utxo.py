from Blockchain.Blockchain import Blockchain
from Utxo.utxo_utils import set_transactions_in_ledger




class Utxo:
    def __init__(self, blockchain: Blockchain) -> None:
        self.ledger = self.get_every_ledger(blockchain)
        
    def get_every_ledger(self, blockchain: Blockchain) -> dict:
        ledger = {}
        for block in blockchain.chain:
            try:
                set_transactions_in_ledger(ledger, block.transactions, blockchain.coinbase_value)
            except ValueError:
                raise ValueError("invalid transactions")
        return ledger
