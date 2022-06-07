import numpy as np
from Node import Node


class Variable(Node):

    def __init__(self, name, size):
        Node.__init__(self, name)
        self.marginal = None
        self.size = size
        self.lastMessage = 1

    def marginal_exe(self):

        self.marginal = np.ones(self.size)
        for array in self.received_message:
            for i in range(len(array)):
                self.marginal[i] = self.marginal[i] * array[i]

        z = np.sum(self.marginal)
        self.marginal = self.marginal / z

        print("Marginal probability on " + self.name + " : " + str(
            self.marginal) + " Z: " + str(z) + " Received message: " + str(self.received_message))
