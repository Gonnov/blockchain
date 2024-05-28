def managePeers(self, peers):
    for peer in peers:
        self.connect_with_node('', peer[1]) #NEED TO REPLACE IP
        if peer not in self.peers:
            self.peers.append(peer)
