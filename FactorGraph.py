import itertools

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
        self.nodes[node1].add_connection(self.nodes[node2])

    def sum_product(self, root):
        self.root = self.nodes[root]
        for e in self.root.connections:
            self.collect(self.root, e)
        self.root.lastMessage = self.root.received_message[0]
        print("--------------------------------------------")
        for e in self.root.connections:
            self.distribute(self.root, e)
        print("--------------------------------------------")
        for i in self.nodes:
            if isinstance(self.nodes[i], Variable):
                self.compute_marginal(i)
        print("--------------------------------------------")

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

    def reset_lastmessage(self):
        for item in self.nodes.items():
            if isinstance(item, Variable):
                item.lastMessage = 1
            else:
                item.lastMessage = {}

    def compute_marginal(self, i):
        if len(self.nodes[i].connections) == 1:
            self.nodes[i].marginal = self.nodes[i].received_message[0]
        else:
            self.nodes[i].marginal = self.nodes[i].received_message[0] * self.nodes[i].received_message[1]
        self.nodes[i].marginal = self.nodes[i].marginal / np.sum(self.nodes[i].marginal)

        print("Marginal probability on " + self.nodes[i].name + " : " + str(self.nodes[i].marginal))

    def send_message(self, sender, receiver):
        if len(sender.connections) == 1 and self.root != sender:
            if isinstance(sender, Variable):
                msg = 1
                receiver.lastMessage[sender.name] = msg
            else:
                msg = sender.weight
                if not isinstance(receiver.lastMessage, int):
                    receiver.lastMessage = [receiver.lastMessage, msg] #da fixare è un po marcio funziona solo con due factor
                else:
                    receiver.lastMessage = msg

        elif self.root == sender:
            sender.lastMessage = 1
        else:
            if isinstance(sender, Variable):
                msg = sender.lastMessage
                if isinstance(msg, int) or isinstance(msg[0], float) or isinstance(msg[0], int):
                    sender.lastMessage = 1
                    receiver.lastMessage[sender.name] = msg
                else:
                    sender.lastMessage = 1

                    giro = 0
                    if giro == 1:
                        msg = np.sum(msg, axis=0)
                    else:
                        msg = [msg[0][i]*msg[1][i] for i in range(len(msg[0]))]

                    receiver.lastMessage[sender.name] = msg
            else:
                marg_mex = []
                for i in sender.lastMessage.keys():
                    index = -1
                    for count, value in enumerate(sender.variables):
                        if value == i:
                            index = count
                            break
                    if isinstance(sender.lastMessage[i], int):
                        marg_mex.append(np.sum(sender.weight, axis=index))
                    else:
                        if len(sender.connections) == 2:
                            marg_mex.append(np.matmul(sender.lastMessage[i], sender.weight))
                        else:
                            marg_mex.append(np.matmul(sender.lastMessage[i], np.sum(sender.weight, axis=index)))

                msg = np.sum(np.array(marg_mex), axis=0)

                sender.lastMessage = {}
                if receiver.lastMessage != 1:
                    receiver.lastMessage = [receiver.lastMessage, msg] #da fixare è un po marcio funziona solo con due factor
                else:
                    receiver.lastMessage = msg

        receiver.received_message.append(msg)

        print("Message (by leaf) send by " + sender.name + " to " + receiver.name + ' : ' + str(msg))

    def send_message_root(self, sender, receiver):

        if self.root != sender and len(sender.connections) == 1:  # useless
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
                    if len(sender.connections) == 2:
                        # print(np.array(sender.lastMessage[i]).shape, np.array(sender.weight).transpose().shape)
                        marg_mex.append(np.matmul(sender.lastMessage[i], np.array(sender.weight).transpose()))
                    else:
                        # print(np.array(sender.lastMessage[i]).shape, np.sum(np.array(sender.weight),
                        # axis=index-1).transpose().shape)
                        marg_mex.append(np.matmul(sender.lastMessage[i],
                                                  np.sum(np.array(sender.weight), axis=index - 1).transpose()))

                msg = np.sum(np.array(marg_mex), axis=0)

                # sender.lastMessage = {}
                receiver.lastMessage = msg

        receiver.received_message.append(msg)

        print("Message (by root) send by " + sender.name + " to " + receiver.name + ' : ' + str(msg))
