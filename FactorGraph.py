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
        self.root.lastmessage = self.root.recivedMessages[0]
        for e in self.root.connections:
            self.distribute(self.root, e)  # todo non passarlo
        for i in self.nodes:
            if isinstance(self.nodes[i], Variable):
                self.computemarginal(self.nodes[i])

    def collect(self, i, j):
        for k in j.connections:
            if k == i:
                continue
            self.collect(j, k)
        self.sendmessage(j, i)

    def distribute(self, i, j):
        self.sendmessage_ritorno(i, j)
        for k in j.connections:
            if k == i:
                continue
            self.distribute(j, k)

    def computemarginal(self, i):
        if len(i.connections) == 1:
            i.marginal = i.recivedMessages[0]
        else:
            i.marginal = i.recivedMessages[0] * i.recivedMessages[1]
        i.marginal = i.marginal / np.sum(i.marginal)
        print("calcolo probabilità marginale su " + i.name + str(i.marginal))

    def sendmessage(self, sender, reciver):

        if len(sender.connections) == 1 and self.root != sender:
            if isinstance(sender, Variable):
                msg = 1
                reciver.lastMessage[sender.name] = msg
            else:
                msg = sender.weight
                reciver.lastMessage = msg

        elif self.root == sender:
            sender.lastMessage = 1
            msg = "SONO LA ROOT"
        else:
            if isinstance(sender, Variable):
                msg = sender.lastMessage
                sender.lastMessage = 1
                reciver.lastMessage[sender.name] = msg
            else:
                marg_mex = []

                for i in sender.lastMessage.keys():
                    index = -1
                    for count, value in enumerate(sender.variables):
                        if value == i:
                            index = count
                            break

                    test = np.sum(sender.weight, axis=(index))
                    marg_mex.append(np.matmul(sender.lastMessage[i], np.sum(sender.weight, axis=(index))))

                    print(marg_mex,test, i)
                msg = np.sum(np.array(marg_mex), axis=0)

                sender.lastMessage = {}
                reciver.lastMessage = msg

        reciver.recivedMessages.append(msg)

        # todo mandare il messaggio

        print("messaggio inviato da " + sender.name + " a " + reciver.name + ' msg: ' + str(msg))

    def sendmessage_ritorno(self, sender, reciver):

        if self.root != sender and len(sender.connections) == 1:
            sender.lastMessage = 1
            msg = "SONO LA ROOT"
        else:
            if isinstance(sender, Variable):
                msg = sender.lastMessage
                sender.lastMessage = 1
                reciver.lastMessage[sender.name] = msg
            else:
                marg_mex = []
                for i in sender.lastMessage.keys():
                    index = -1
                    for count, value in enumerate(sender.variables):
                        if value == i:
                            index = count
                            break
                    test = np.sum(np.array(sender.weight), axis=(index - 1)).transpose()
                    print(np.array(sender.lastMessage[i]).shape, test.shape)
                    marg_mex.append(
                        np.matmul(sender.lastMessage[i], np.sum(np.array(sender.weight), axis=(index - 1)).transpose()))

                msg = np.sum(np.array(marg_mex), axis=0)

                sender.lastMessage = {}
                reciver.lastMessage = msg

        reciver.recivedMessages.append(msg)

        # todo mandare il messaggio

        print("messaggio di ritorno inviato da " + sender.name + " a " + reciver.name + ' msg: ' + str(msg))
