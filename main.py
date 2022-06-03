from FactorGraph import FactorGraph


def main():

    graph = FactorGraph()

    graph.add_node("x1", 2)
    graph.add_node("x2", 3)
    graph.add_node("x3", 2)
    graph.add_node("x4", 2)

    graph.add_factor("f3", [
        [0.2, 0.8]
    ], ["x3"])

    graph.add_factor("f4", [
        [0.5, 0.5]
    ], ["x4"])

    graph.add_factor("f12", [
        [[0.8, 0.2], [0.2, 0.8], [0.5, 0.5]]
    ], ["x2", "x1"])

    graph.add_factor("f342", [
        [[0.3, 0.5, 0.2], [0.1, 0.1, 0.8]], [[0.9, 0.05, 0.05], [0.2, 0.7, 0.1]]
    ], ["x4", "x3", "x2"])

    graph.add_connection("x3", "f3")
    graph.add_connection("x4", "f4")

    graph.add_connection("x2", "f12")
    graph.add_connection("x1", "f12")

    graph.add_connection("x3", "f342")
    graph.add_connection("x4", "f342")
    graph.add_connection("x2", "f342")

    graph.sum_product("x1")


if __name__ == '__main__':
    main()
