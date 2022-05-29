from Node import Node


class Factor(Node):

    def __init__(self, name, weight):
        self.p = weight
        Node.__init__(self, name)
