def managePeers(self, data):
    for peer in data:
        print("PEER -> ", [peer[0], peer[1]], "SELF PEER -> ", self.peers)
        if self.ip == peer[0] and self.port == peer[1]:
            continue
        elif [peer[0], peer[1]] in self.peers:
            continue
        else:
            self.connect_with_node('', peer[1])
        # print(peer)
    self.peers = data