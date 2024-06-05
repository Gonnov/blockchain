from Blockchain.Blockchain import Blockchain

def remove_transaction_from_mempool(mempool, block):
    for transaction in block.transactions:
        if transaction in mempool:
            mempool.remove(transaction)
    return mempool


def manageBlockchain(self, typename: str, blockchain: Blockchain):
    if len(self.blockchain.chain) > len(blockchain.chain):
        return False
    if blockchain.check_whole_blockchain() is False:
        return False
    self.blockchain = blockchain
    for block in self.blockchain.chain:
        self.mempool = remove_transaction_from_mempool(self.mempool, block)

    
    