def removePeer(self, peer_to_delete):
    for peer in self.peers:
        if peer[0] == peer_to_delete[0] and peer[1] == peer_to_delete[1]:
            self.peers.remove(peer)
            break