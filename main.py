from FactorGraph import FactorGraph


def main():
    graph = FactorGraph()

    graph.addNode("a", 2)
    graph.addNode("b", 3)

    graph.addFactor("f1", [
        [0.8, 0.2],
        [0.2, 0.8],
        [0.5, 0.5]
    ], ["a", "b"])

    graph.addConnection("a", "f1")
    graph.addConnection("f1", "b")

    graph.sumProduct("a")


if __name__ == '__main__':
    main()
