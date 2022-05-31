from Factor import Factor
from Variable import Variable
import numpy as np


class FactorGraph:

    def __init__(self):
        self.nodes = {}
        self.root = None

    def addNode(self, name, nstates):
        self.nodes[name] = Variable(name, nstates)

    def addFactor(self, name, weight, variable):
        self.nodes[name] = Factor(name, weight, variable)

    def addConnection(self, node1, node2):
        try:
            self.nodes[node1].addConnection(self.nodes[node2])
        except:
            print(self.nodes)

    def sumProduct(self, root):
        self.root = self.nodes[root]
        for e in self.root.connections:
            self.collect(self.root, e)
        for e in self.root.connections:
            self.distribute(self.root, e)  # todo non passarlo
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

    def sendmessage(self, sender, reciver):

        if len(sender.connections) == 1 and self.root != sender:
            if isinstance(sender, Variable):
                msg = 1
                reciver.lastMessage[sender.name] = msg
            else:
                msg = sender.weigth
                reciver.lastMessage = msg

        elif self.root == sender:
            sender.lastMessage = 1
            msg = "SONO LA ROOT"
        else:
            if isinstance(sender, Variable):
                # msg = np.sum(i.weight, axis=i.variables.index(j.name) - 1) * j.lastMessage
                msg = sender.lastMessage
                sender.lastMessage = 1
                reciver.lastMessage[sender.name] = msg
            else:
                # if len(j.lastMessage) == 1:
                #    msg = j.lastMessage
                # else:
                #    msg = np.sum(np.array(j.lastMessage), axis=0)

                marg_mex = []
                for i in sender.lastMessage.keys():
                    index = -1
                    for count, value in enumerate(sender.connections):
                        if value.name == i:
                            index = count
                            break
                    marg_mex.append(np.sum(sender.weight, axis=(index-1)) * sender.lastMessage[i])

                msg = np.sum(np.array(marg_mex), axis=0)

                sender.lastMessage = {}
                reciver.lastMessage = msg

        reciver.recivedMessages.append(msg)

        # todo mandare il messaggio

        print("messaggio inviato da " + sender.name + " a " + reciver.name + ' msg: ' + str(msg))
