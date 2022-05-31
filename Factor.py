from Node import Node


class Factor(Node):

    def __init__(self, name, weight, variables):
        self.weight = weight
        Node.__init__(self, name)
        self.variables = variables
        self.lastMessage = {}

