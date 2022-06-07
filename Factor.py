from Node import Node


class Factor(Node):

    def __init__(self, name, weight, variables):
        Node.__init__(self, name)
        self.weight = weight
        self.org = weight
        self.variables = variables
        self.lastMessage = {}
