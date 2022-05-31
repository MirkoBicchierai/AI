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


def main2():
    graph = FactorGraph()

    graph.addNode("x1", 2)
    graph.addNode("x2", 3)
    graph.addNode("x3", 2)
    graph.addNode("x4", 2)

    graph.addFactor("f3", [
        [0.2, 0.8]
    ], ["x3"])

    graph.addFactor("f4", [
        [0.5, 0.5]
    ], ["x4"])

    graph.addFactor("f12", [
        [[0.8, 0.2], [0.2, 0.8], [0.5, 0.5]]
    ], ["x2", "x1"])

    graph.addFactor("f342", [
        [[0.3, 0.5, 0.2], [0.1, 0.1, 0.8]], [[0.9, 0.05, 0.05], [0.2, 0.7, 0.1]]
    ], ["x4", "x3", "x2"])

    graph.addConnection("x3", "f3")
    graph.addConnection("x4", "f4")

    graph.addConnection("x2", "f12")
    graph.addConnection("x1", "f12")

    graph.addConnection("x3", "f342")
    graph.addConnection("x4", "f342")
    graph.addConnection("x2", "f342")

    graph.sumProduct("x1")


if __name__ == '__main__':
    main2()
