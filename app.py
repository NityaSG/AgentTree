class CalculatorBase:
    def __init__(self, output_number):
        self.input_number = None  # Will be set from the output of another node
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
        self.inputs = []  # List of Node names whose output is input to this Node
        self.output = None

    def add_input(self, node_name):
        self.inputs.append(node_name)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.execution_order = []

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_edge(self, from_node_name, to_node_name):
        self.nodes[to_node_name].add_input(from_node_name)

    def find_execution_order(self):
        visited = set()
        self.execution_order = []

        def visit(node_name):
            if node_name not in visited:
                visited.add(node_name)
                for next_node_name in self.nodes[node_name].inputs:
                    visit(next_node_name)
                self.execution_order.append(node_name)

        for node_name in self.nodes:
            visit(node_name)

    def execute(self):
        self.find_execution_order()
        for node_name in self.execution_order:
            node = self.nodes[node_name]
            if node.inputs:
                # For simplicity, assuming a single input
                input_node_name = node.inputs[0]
                input_node = self.nodes[input_node_name]
                node.calculator.input_number = input_node.output
            node.output = node.calculator.calculate()

# Example usage
graph = Graph()

# Creating nodes with operations
graph.add_node(Node(AddCalculator(5), 'add1'))
graph.add_node(Node(MultiplyCalculator(2), 'mul1'))

# Defining connections (edges)
graph.add_edge('add1', 'mul1')

# Setting an initial input value
graph.nodes['add1'].calculator.input_number = 10

# Execute the graph
graph.execute()

# Accessing results
print(f"Output of add1: {graph.nodes['add1'].output}")  # Should be 15
print(f"Output of mul1: {graph.nodes['mul1'].output}")  # Should be 30
