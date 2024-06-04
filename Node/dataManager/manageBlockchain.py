from Blockchain.Blockchain import Blockchain

def remove_transaction_from_mempool(mempool, block):
    for transaction in block.transactions:
        if transaction in mempool:
            mempool.remove(transaction)
    return mempool

def manageBlockchain(self, blockchain: Blockchain):
    for block in blockchain.chain:
        print(block.transactions)
    if len(self.blockchain.chain) > len(blockchain.chain):
        return 
    if blockchain.check_whole_blockchain() is False:
        return
    for block in blockchain.chain:
        if block not in self.blockchain.chain and block.previous_hash is not None:
            print(block.transactions)
            self.blockchain.chain.append(block)
            self.mempool = remove_transaction_from_mempool(self.mempool, block)
    
    