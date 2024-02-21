class CalculatorBase:
    def __init__(self, output_number):
        self.input_number = None
        self.output_number = output_number

    def calculate(self):
        raise NotImplementedError("Subclass must implement abstract method")

class AddCalculator(CalculatorBase):
    def calculate(self):
        return self.input_number + self.output_number

class MultiplyCalculator(CalculatorBase):
    def calculate(self):
        return self.input_number * self.output_number

class Node:
    def __init__(self, calculator, name):
        self.calculator = calculator
        self.name = name
        self.inputs = []
        self.output = None

    def add_input(self, node_name):
        self.inputs.append(node_name)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.initial_nodes = []
        self.final_nodes = []

    def add_node(self, node, is_initial=False, is_final=False):
        self.nodes[node.name] = node
        if is_initial:
            self.initial_nodes.append(node.name)
        if is_final:
            self.final_nodes.append(node.name)

    def add_edge(self, from_node_name, to_node_name):
        self.nodes[to_node_name].add_input(from_node_name)

    def set_initial_input(self, node_name, input_value):
        if node_name in self.nodes:
            self.nodes[node_name].calculator.input_number = input_value

    def execute(self):
        for node_name in self.nodes:
            node = self.nodes[node_name]
            if node.inputs:
                for input_node_name in node.inputs:
                    input_node = self.nodes[input_node_name]
                    node.calculator.input_number = input_node.output
            node.output = node.calculator.calculate()

# Example usage
graph = Graph()

# Creating nodes with operations and marking initial and final states
graph.add_node(Node(AddCalculator(5), 'add1'), is_initial=True)
graph.add_node(Node(MultiplyCalculator(2), 'mul1'), is_final=True)

# Defining connections (edges)
graph.add_edge('add1', 'mul1')

# Setting the main input for the initial node
graph.set_initial_input('add1', 10)

# Execute the graph
graph.execute()

# Accessing results from final nodes
for final_node_name in graph.final_nodes:
    print(f"Output of {final_node_name}: {graph.nodes[final_node_name].output}")
