

from Blockchain.Blockchain import Blockchain
from transaction.CoinbaseTransaction import CoinbaseTransaction
from transaction.Transaction import Transaction
from transaction.TransactionData import TransactionData
from user.Wallet import Wallet


def make_basic_coinbase_transaction(amount: int):
    user = Wallet()
    coinbase_transaction = CoinbaseTransaction(amount, user.public_key)
    return coinbase_transaction

def make_basic_transaction():
    first_user = Wallet()
    second_user = Wallet()
    transactionData = TransactionData(second_user.public_key, first_user.public_key ,10)
    sender_signature = second_user.sign_transaction(transactionData.serialize())
    transaction = Transaction(transactionData, sender_signature)
    return transaction

def make_coinbase_transaction(user: Wallet, amount: int):
    coinbase_transaction = CoinbaseTransaction(amount, user.public_key, 1)
    return coinbase_transaction

def make_transaction(sender: Wallet, receiver: Wallet, amount: int):
    transactionData = TransactionData(sender.public_key, receiver.public_key ,amount)
    sender_signature = sender.sign_transaction(transactionData.serialize())
    transaction = Transaction(transactionData, sender_signature)
    return transaction

def setup_blockchain_n_blocks(n: int):
    blockchain = Blockchain()
    #add block test
    i = 0
    first_user = Wallet()
    second_user = Wallet()
    third_user = Wallet()
    while i + 1 < n:
        coinbaseTransaction = make_coinbase_transaction(first_user, blockchain.coinbase_value)
        first_transaction = make_transaction(first_user, second_user, blockchain.coinbase_value)
        second_transaction = make_transaction(second_user, third_user, blockchain.coinbase_value/3)
        thrid_transaction = make_transaction(second_user, first_user, blockchain.coinbase_value/3)
        blockchain.add_block([coinbaseTransaction, first_transaction, second_transaction, thrid_transaction])
        i += 1
    
    return blockchain