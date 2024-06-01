from Blockchain.Blockchain import Blockchain
from Utxo.utxo_utils import set_transactions_in_ledger




class Utxo:
    """
    Represents the Unspent Transaction Output (UTXO) set of the blockchain.

    Attributes:
        ledger (dict): The dictionary representing the UTXO set.

    Methods:
        get_every_ledger(blockchain): Constructs the UTXO set from the blockchain.
    """

    def __init__(self, blockchain: Blockchain) -> None:
        """
        Initialize the UTXO set.

        Args:
            blockchain (Blockchain): The blockchain from which to construct the UTXO set.

        Attributes:
            ledger (dict): The dictionary representing the UTXO set.
        """
        self.ledger = self.get_every_ledger(blockchain)
        
    def get_every_ledger(self, blockchain: Blockchain) -> dict:
        """
        Constructs the UTXO set from the blockchain.

        Iterates through the blockchain to create a dictionary representing the UTXO set,
        by including all valid transactions.

        Args:
            blockchain (Blockchain): The blockchain from which to construct the UTXO set.

        Returns:
            dict: The dictionary representing the UTXO set.

        Raises:
            ValueError: If any invalid transactions are found in the blockchain.
        """

        ledger = {}
        for block in blockchain.chain:
            try:
                set_transactions_in_ledger(ledger, block.transactions, blockchain.coinbase_value)
            except ValueError:
                raise ValueError("invalid transactions")
        return ledger

