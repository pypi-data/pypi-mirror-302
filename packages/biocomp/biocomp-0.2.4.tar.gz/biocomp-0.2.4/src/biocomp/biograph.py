import yaml
import graphviz


class Molecule:
    """
    Represents a molecule in the biological system.

    Attributes:
        type (str): The type of the molecule.
        name (str): The name of the molecule.

    Methods:
        __init__(self, type, name): Initializes a new Molecule object.
        __repr__(self): Returns a string representation of the Molecule object.
    """

    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self):
        return f"{self.type}({self.name})"


class LogicGate:
    """
    Represents a logic gate in the biological system.

    Attributes:
        gate_type (str): The type of the logic gate (e.g., 'NOT', 'AND', 'OR').
        input1 (Molecule): The first input molecule of the logic gate.
        input2 (Molecule, optional): The second input molecule of the logic gate.
        output (Molecule): The output molecule of the logic gate.

    Methods:
        __init__(self, gate_type, input1, output, input2=None): Initializes a new LogicGate object.
        __repr__(self): Returns a string representation of the LogicGate object.
    """

    def __init__(self, gate_type, input1, output, input2=None):
        self.gate_type = gate_type
        self.input1 = input1
        self.input2 = input2
        self.output = output

    def __repr__(self):
        if self.gate_type == 'NOT':
            return f"{self.gate_type} Gate(Input: {self.input1.name}, Output: {self.output.name})"
        return f"{self.gate_type} Gate(Input1: {self.input1.name}, Input2: {self.input2.name}, Output: {self.output.name})"


class BiologicalSystem:
    """
    Represents a biological system containing molecules and logic gates.

    Attributes:
        name (str): The name of the biological system.
        logic_gates (list of LogicGate): A list of logic gates in the biological system.
        molecules (list of Molecule): A list of molecules in the biological system.

    Methods:
        __init__(self, name, logic_gates, molecules): Initializes a new BiologicalSystem object.
        __repr__(self): Returns a string representation of the BiologicalSystem object.
    """

    def __init__(self, name, logic_gates, molecules):
        self.name = name
        self.logic_gates = logic_gates
        self.molecules = molecules

    def __repr__(self):
        return f"Biological System({self.name}) with Logic Gates: {self.logic_gates} and Molecules: {self.molecules}"


class Simulation:
    """
    Represents a simulation of a biological system.

    Attributes:
        system (BiologicalSystem): The biological system being simulated.
        conditions (dict): A dictionary of simulation conditions.
        outputs (dict): A dictionary of expected simulation outputs.

    Methods:
        __init__(self, system, conditions, outputs): Initializes a new Simulation object.
        run(self): Runs the simulation and prints the simulation conditions and expected outputs.

    """

    def __init__(self, system, conditions, outputs):
        self.system = system
        self.conditions = conditions
        self.outputs = outputs

    def run(self):
        print(f"Running simulation for {self.system.name}")
        print(f"Conditions: {self.conditions}")
        print(f"Expected Outputs: {self.outputs}")


def visualize_biological_system(bio_system):
    """
    Visualizes the biological system using the Graphviz library.

    Args:
        bio_system (BiologicalSystem): The biological system to be visualized.

    """

    dot = graphviz.Digraph(comment=bio_system.name)

    # Add nodes for molecules
    for molecule in bio_system.molecules:
        dot.node(molecule.name, f'{molecule.name} ({molecule.type})')

    # Add nodes and edges for logic gates
    for gate in bio_system.logic_gates:
        gate_label = f'{gate.gate_type} Gate'
        dot.node(gate_label)
        dot.edge(gate.input1.name, gate_label)
        if gate.gate_type != 'NOT':
            dot.edge(gate.input2.name, gate_label)
        dot.edge(gate_label, gate.output.name)

    dot.render('bio_system_graph', format='png', view=True)


def main(yaml_file):
    """
    Parses a YAML file containing information about a biological system, runs a simulation, and visualizes the biological system.

    Args:
        yaml_file (str): The path to the YAML file containing information about the biological system.

    """

    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    # Parse molecules
    molecules = {m['name']: Molecule(type=m['type'], name=m['name']) for m in data['molecules']}

    # Parse logic gates
    logic_gates = []
    for lg in data['logic_gates']:
        if lg['gate_type'] == 'NOT':
            logic_gate = LogicGate(gate_type=lg['gate_type'],
                                       input1=molecules[lg['input1']],
                                       output=molecules[lg['output']])
        else:
            logic_gate = LogicGate(gate_type=lg['gate_type'],
                                       input1=molecules[lg['input1']],
                                       input2=molecules[lg['input2']],
                                       output=molecules[lg['output']])
        logic_gates.append(logic_gate)

    # Create Biological System
    bio_system = BiologicalSystem(name=data['biological_system']['name'], logic_gates=logic_gates,
                                  molecules=list(molecules.values()))

    # Create and run simulation
    simulation = Simulation(system=bio_system, conditions=data['simulation']['conditions'],
                            outputs=data['simulation']['outputs'])
    simulation.run()

    # Visualize the biological system
    visualize_biological_system(bio_system)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
        main(yaml_file)
    else:
        print("Please provide a YAML file as an argument.")