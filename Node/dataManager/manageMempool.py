def manageMempool(self, mempool):
    for transaction in mempool:
        if transaction not in self.mempool:
            if transaction.check_transaction_validity():
                self.mempool.append(transaction)
