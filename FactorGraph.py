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

        print("-----------------------------------------------")
        for e in self.root.connections:
            self.distribute(self.root, e)
        print("-----------------------------------------------")
        for i in self.nodes:
            if isinstance(self.nodes[i], Variable):
                self.compute_marginal(i)
        print("-----------------------------------------------")

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
        self.nodes[i].marginal_exe()

    def send_message(self, sender, receiver):

        if len(sender.connections) == 1 and self.root != sender:
            if isinstance(sender, Variable):
                msg = 1
                receiver.lastMessage[sender.name] = msg
            else:
                msg = sender.weight
                if not isinstance(receiver.lastMessage, int):
                    receiver.lastMessage = [receiver.lastMessage, msg]
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
                    msg = np.multiply(msg[0], msg[1])
                    receiver.lastMessage[sender.name] = msg
            else:
                mex = []
                for i in sender.lastMessage.keys():
                    index = -1
                    for count, value in enumerate(sender.variables):
                        if value == i:
                            index = count
                            break
                    if isinstance(sender.lastMessage[i], int):
                        mex.append(np.sum(sender.weight, axis=index))
                    else:
                        if len(sender.connections) == 2:
                            print(sender.lastMessage[i], sender.weight)
                            mex.append(np.matmul(sender.lastMessage[i], sender.weight))
                        else:
                            mex.append(np.matmul(sender.lastMessage[i], np.sum(sender.weight, axis=index)))

                msg = np.sum(np.array(mex), axis=0)

                sender.lastMessage = {}
                if receiver.lastMessage != 1:
                    receiver.lastMessage = [receiver.lastMessage, msg]
                else:
                    receiver.lastMessage = msg

        receiver.received_message.append(msg)

        print("Message (by leaf) send by " + sender.name + " to " + receiver.name + ' : ' + str(msg))

    def send_message_root(self, sender, receiver):

        if isinstance(sender, Variable):
            msg = sender.lastMessage
            receiver.lastMessage[sender.name] = msg
        else:
            mex = []
            i = list(sender.lastMessage.keys())[0]
            index = -1
            for count, value in enumerate(sender.variables):
                if value == receiver.name:
                    index = count
                    break
            if len(sender.connections) == 2:
                if np.array(sender.lastMessage[i]).shape[0] != np.array(sender.weight).shape[0]:
                    mex.append(np.matmul(sender.lastMessage[i], np.array(sender.weight).transpose()))
                else:
                    mex.append(np.matmul(sender.lastMessage[i], np.array(sender.weight)))

            else:
                mex.append(np.matmul(sender.lastMessage[i],
                                     np.sum(np.array(sender.weight), axis=index).transpose()))

            msg = np.sum(np.array(mex), axis=0)
            receiver.lastMessage = msg

        receiver.received_message.append(msg)

        print("Message (by root) send by " + sender.name + " to " + receiver.name + ' : ' + str(msg))
