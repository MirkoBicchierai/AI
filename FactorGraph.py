from Factor import Factor
from Variable import Variable


class FactorGraph:

    def __init__(self):
        self.nodes = {}

    def addNode(self, name, nstates):
        self.nodes[name] = Variable(name, nstates)

    def addFactor(self, name, weight):
        self.nodes[name] = Factor(name, weight)

    def addConnection(self, node1, node2):
        try:
            self.nodes[node1].addConnection(self.nodes[node2])
        except:
            print(self.nodes)

    def sumProduct(self, root):
        root = self.nodes[root]


