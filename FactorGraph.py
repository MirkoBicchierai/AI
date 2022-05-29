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
        for e in root.connections:
            self.collect(root, e)
        for e in root.connections:
            self.distribute(root, e)
        for i in self.nodes:
            self.computemarginal(i)

    def collect(self, i, j):
        for k in j.connections:
            if k == i:
                continue
            self.collect(j, k)
        self.sendmessage(j, i)

    def distribute(self, i, j):
        self.sendmessage(i, j)
        for k in j.connections:
            if k == i:
                continue
            self.distribute(j, k)

    def computemarginal(self, i):
        print("calcolo probabilità marginale su " + i)

    def sendmessage(self, j, i):
        print("messaggio inviato da " + j.name + " a " + i.name)
