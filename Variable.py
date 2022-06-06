import numpy as np
from Node import Node


class Variable(Node):

    def __init__(self, name, size):
        Node.__init__(self, name)
        self.marginal = None
        self.size = size
        self.lastMessage = 1

    def marginal_exe(self):

        if len(self.connections) == 1:
            self.marginal = self.received_message[0]
        else:
            self.marginal = self.received_message[0] * self.received_message[1]

        z = np.sum(self.marginal)
        self.marginal = self.marginal / z

        # print("message on " + self.name + " : " + str(self.received_message))
        print("Marginal probability on " + self.name + " : " + str(
            self.marginal) + " Z: " + str(z))
        # np.around(self.marginal, decimals=4)
