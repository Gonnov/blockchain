

def manageNewBlock(self, blockchain: Blockchain):
    if len(self.blockchain.chain) > len(blockchain.chain):
        return 
    if blockchain.check_whole_blockchain() is False:
        return
    for block in blockchain.chain:
        if block not in self.blockchain.chain and block.previous_hash is not None:
            print("block added from peers")
            self.blockchain.chain.append(block)
            self.mempool = remove_transaction_from_mempool(self.mempool, block)