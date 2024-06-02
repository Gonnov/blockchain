from transaction.Transaction import Transaction
import binascii

def add_to_receiver(ledger: dict, transaction: Transaction) -> None:
    receiver_public_key = transaction.transaction_outputs.receiver_public_key
    hex_public_key = binascii.hexlify(receiver_public_key).decode('utf-8')
    amount = transaction.transaction_outputs.amount
    ledger.setdefault(hex_public_key, 0)
    ledger[hex_public_key] += amount
    
def take_to_sender(ledger: dict, transaction: Transaction) -> None:
    sender_public_key = transaction.transaction_inputs.sender_public_key
    hex_public_key = binascii.hexlify(sender_public_key).decode('utf-8')
    amount = transaction.transaction_outputs.amount
    ledger[hex_public_key] -= amount
    if (ledger[hex_public_key] == 0):
        del ledger[hex_public_key]
    elif (ledger[hex_public_key] < 0):
        raise ValueError("not enough funds")
    
def manage_first_transaction(ledger: dict, first_transaction, coinbase_value) -> None:
    if first_transaction is None:
        return "no transaction"
    if first_transaction.check_transaction_validity(coinbase_value) is False:
        raise ValueError("invalid transactions")
    add_to_receiver(ledger, first_transaction)

def manage_rest_transactions(ledger: dict, transactions: list) -> None:
    for transaction in transactions:
        if transaction.check_transaction_validity() is False:
            raise ValueError("invalid transactions")
        add_to_receiver(ledger, transaction)
        try:
            take_to_sender(ledger, transaction)
        except ValueError:
            return ValueError

def set_transactions_in_ledger(ledger: dict, transaction, coinbase_value) -> None:
    try:
        if manage_first_transaction(ledger, transaction[0], coinbase_value) == "no transaction":
            return
    except ValueError:
        raise ValueError("invalid transactions")
    try:
        manage_rest_transactions(ledger, transaction[1:])
    except ValueError:
        raise ValueError("invalid transactions")