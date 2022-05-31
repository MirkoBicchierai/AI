class Node:

    def __init__(self, name):
        self.name = name
        self.connections = []
        self.lastMessage = None
        self.recivedMessages = []

    def addConnection(self, to_node):
        self.connections.append(to_node)
        to_node.connections.append(self)
