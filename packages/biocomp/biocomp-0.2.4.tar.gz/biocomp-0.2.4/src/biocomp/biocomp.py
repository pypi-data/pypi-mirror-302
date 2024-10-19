import yaml
import matplotlib.pyplot as plt
import numpy as np


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
        conditions (dict): A dictionary containing the simulation conditions.
        outputs (list of str): A list of expected output names.

    Methods:
        __init__(self, system, conditions, outputs): Initializes a new Simulation object.
        run(self): Runs the simulation and prints the simulation details.

    """
    def __init__(self, system, conditions, outputs):
        self.system = system
        self.conditions = conditions
        self.outputs = outputs

    def run(self):
        print(f"Running simulation for {self.system.name}")
        print(f"Conditions: {self.conditions}")
        print(f"Expected Outputs: {self.outputs}")




def run_simulation(simulation: Simulation):
    """
    Runs a simulation and plots the output levels.

    Args:
        simulation (Simulation): The simulation to be run.

    Returns:
        None
    """
    time = np.linspace(0, simulation.conditions["time"], 100)  # Generate 100 time points
    output_levels = np.random.rand(100)  # Random values to simulate protein output level

    plt.figure()
    plt.plot(time, output_levels, label=f"{simulation.outputs[0]}")
    plt.title(f"Simulation: {simulation.system.name}")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Output Level")
    plt.legend()
    plt.show()


def main(yaml_file):
    """
    Parses a YAML file, creates a biological system, and runs a simulation.

    Args:
        yaml_file (str): The path to the YAML file containing the biological system data.

    Returns:
        None
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
    bio_system = BiologicalSystem(name=data['biological_system']['name'], logic_gates=logic_gates, molecules=list(molecules.values()))

    # Create and run simulation
    simulation = Simulation(system=bio_system, conditions=data['simulation']['conditions'], outputs=data['simulation']['outputs'])
    simulation.run()
    run_simulation(simulation)



if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
        main(yaml_file)
    else:
        print("Please provide a YAML file as an argument.")