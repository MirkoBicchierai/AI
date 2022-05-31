from Factor import Factor
from Variable import Variable
import numpy as np


class FactorGraph:

    def __init__(self):
        self.nodes = {}
        self.root = None

    def add_node(self, name, n_states):
        self.nodes[name] = Variable(name, n_states)

    def add_factor(self, name, weight, variable):
        self.nodes[name] = Factor(name, weight, variable)

    def add_connection(self, node1, node2):
        self.nodes[node1].addConnection(self.nodes[node2])

    def sum_product(self, root):
        self.root = self.nodes[root]
        for e in self.root.connections:
            self.collect(self.root, e)
        self.root.lastMessage = self.root.recivedMessages[0]
        for e in self.root.connections:
            self.distribute(self.root, e)
        for i in self.nodes:
            if isinstance(self.nodes[i], Variable):
                self.compute_marginal(i)

    def collect(self, i, j):
        for k in j.connections:
            if k == i:
                continue
            self.collect(j, k)
        self.send_message(j, i)

    def distribute(self, i, j):
        self.send_message_root(i, j)
        for k in j.connections:
            if k == i:
                continue
            self.distribute(j, k)

    def compute_marginal(self, i):
        if len(self.nodes[i].connections) == 1:
            self.nodes[i].marginal = self.nodes[i].recivedMessages[0]
        else:
            self.nodes[i].marginal = self.nodes[i].recivedMessages[0] * self.nodes[i].recivedMessages[1]
        self.nodes[i].marginal = self.nodes[i].marginal / np.sum(self.nodes[i].marginal)
        print("Marginal probability on " + self.nodes[i].name + " : " + str(self.nodes[i].marginal))

    def send_message(self, sender, receiver):

        if len(sender.connections) == 1 and self.root != sender:
            if isinstance(sender, Variable):
                msg = 1
                receiver.lastMessage[sender.name] = msg
            else:
                msg = sender.weight
                receiver.lastMessage = msg

        elif self.root == sender:
            sender.lastMessage = 1
        else:
            if isinstance(sender, Variable):
                msg = sender.lastMessage
                sender.lastMessage = 1
                receiver.lastMessage[sender.name] = msg
            else:
                marg_mex = []

                for i in sender.lastMessage.keys():
                    index = -1
                    for count, value in enumerate(sender.variables):
                        if value == i:
                            index = count
                            break
                    marg_mex.append(np.matmul(sender.lastMessage[i], np.sum(sender.weight, axis=index)))
                msg = np.sum(np.array(marg_mex), axis=0)

                sender.lastMessage = {}
                receiver.lastMessage = msg

        receiver.recivedMessages.append(msg)

        print("Message (by leaf) send by " + sender.name + " to " + receiver.name + ' : ' + str(msg))

    def send_message_root(self, sender, receiver):

        if self.root != sender and len(sender.connections) == 1:
            sender.lastMessage = 1
        else:
            if isinstance(sender, Variable):
                msg = sender.lastMessage
                sender.lastMessage = 1
                receiver.lastMessage[sender.name] = msg
            else:
                marg_mex = []
                for i in sender.lastMessage.keys():
                    index = -1
                    for count, value in enumerate(sender.variables):
                        if value == i:
                            index = count
                            break
                    marg_mex.append(
                        np.matmul(sender.lastMessage[i], np.sum(np.array(sender.weight), axis=(index - 1)).transpose()))

                msg = np.sum(np.array(marg_mex), axis=0)

                sender.lastMessage = {}
                receiver.lastMessage = msg

        receiver.recivedMessages.append(msg)

        print("Message (by root) send by " + sender.name + " to " + receiver.name + ' : ' + str(msg))
