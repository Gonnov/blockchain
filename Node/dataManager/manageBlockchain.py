from Blockchain.Blockchain import Blockchain

def manageBlockchain(self, blockchain: Blockchain):
    if len(self.blockchain) < len(blockchain):
        return 
    if blockchain.check_whole_blockchain() is False:
        return
    for block in blockchain.chain:
        if block not in self.blockchain.chain:
            self.blockchain.chain.append(block)
    
    