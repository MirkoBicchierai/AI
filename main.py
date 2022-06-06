from FactorGraph import FactorGraph


def main_3():
    graph = FactorGraph()

    graph.add_node("X1", 2)
    graph.add_node("X2", 2)
    graph.add_node("X3", 2)

    graph.add_factor("f1",
                     [0.1, 0.9]
                     , ["X1"])

    graph.add_factor("f2",
                     [0.1, 0.9]
                     , ["X2"])

    graph.add_factor("f3",
                     [0.9, 0.1]
                     , ["X3"])

    graph.add_factor("f4", [
        [0.8, 0.2], [0.8, 0.2]
    ], ["X2", "X1"])

    graph.add_factor("f5", [
        [1, 0], [0, 1]
    ], ["X3", "X2"])

    graph.add_connection("X1", "f1")
    graph.add_connection("X1", "f4")
    graph.add_connection("X2", "f4")
    graph.add_connection("X2", "f5")
    graph.add_connection("X2", "f2")
    graph.add_connection("X3", "f5")
    graph.add_connection("X3", "f3")

    graph.sum_product()

    graph.direct_marginal()


def main():
    graph = FactorGraph()

    graph.add_node("A", 2)
    graph.add_node("B", 3)
    graph.add_node("C", 2)
    graph.add_node("D", 4)
    graph.add_node("E", 2)

    graph.add_factor("f3", [
        0.2, 0.8
    ], ["C"])

    graph.add_factor("f4_", [
        0.1, 0.2, 0.2, 0.5
    ], ["D"])

    graph.add_factor("f45", [
        [0.2, 0.8], [0.3, 0.7], [0.1, 0.9], [0.35, 0.65]
    ], ["D", "E"])

    graph.add_factor("f12", [
        [0.8, 0.2], [0.2, 0.8], [0.5, 0.5]
    ], ["B", "A"])

    graph.add_factor("f342", [
        [
            [0.3, 0.5, 0.2], [0.1, 0.1, 0.8], [0.2, 0.6, 0.2], [0.1, 0.7, 0.2]
        ], [
            [0.9, 0.05, 0.05], [0.2, 0.7, 0.1], [0.4, 0.4, 0.2], [0.1, 0.1, 0.8]
        ]
    ], ["D", "C", "B"])

    graph.add_connection("C", "f3")
    graph.add_connection("D", "f45")
    graph.add_connection("E", "f45")
    graph.add_connection("D", "f4_")
    graph.add_connection("B", "f12")
    graph.add_connection("A", "f12")
    graph.add_connection("C", "f342")
    graph.add_connection("D", "f342")
    graph.add_connection("B", "f342")

    graph.sum_product()
    graph.direct_marginal()


def main_2():
    graph = FactorGraph()

    graph.add_node("x1", 2)
    graph.add_node("x2", 3)

    graph.add_factor("f12", [
        [0.8, 0.2], [0.2, 0.8], [0.5, 0.5]
    ], ["x2", "x1"])

    graph.add_connection("x2", "f12")
    graph.add_connection("x1", "f12")

    graph.sum_product()
    graph.direct_marginal()


if __name__ == '__main__':
    main()
