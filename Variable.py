from Node import Node


class Variable(Node):

    def __init__(self, name, size):
        self.marginal = None
        self.size = size
        Node.__init__(self, name)
        self.lastMessage = 1
