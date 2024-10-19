import argparse
import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
import graphviz
from typing import List, Dict


# Definicje struktur danych
class Simulation:
    def __init__(self, name: str, grid_size: int, steps: int, diffusion_coefficient: float,
                 reaction_rate: float, k: float, initial_u_value: float, initial_v_value: float,
                 initial_radius: int, conditions: Dict[str, float], outputs: List[str]):
        self.name = name
        self.grid_size = grid_size
        self.steps = steps
        self.diffusion_coefficient = diffusion_coefficient
        self.reaction_rate = reaction_rate
        self.k = k
        self.initial_u_value = initial_u_value
        self.initial_v_value = initial_v_value
        self.initial_radius = initial_radius
        self.conditions = conditions
        self.outputs = outputs


def simulate_reaction_diffusion(sim: Simulation):
    n = sim.grid_size
    steps = int(sim.conditions['time'] * 1000)  # assuming "time" in conditions is in days, convert to appropriate steps

    # Adjust diffusion coefficient and reaction rate based on temperature and humidity
    D = sim.diffusion_coefficient * (sim.conditions['temperature'] / 25.0)  # Normalize to room temperature
    f = sim.reaction_rate * (sim.conditions['humidity'] / 100.0)  # Normalize to 100% humidity
    k = sim.k
    initial_u_value = sim.initial_u_value
    initial_v_value = sim.initial_v_value
    initial_radius = sim.initial_radius

    u = np.ones((n, n))
    v = np.zeros((n, n))

    # Inicjalizacja w centrum reaktora
    r = initial_radius
    u[n//2-r:n//2+r, n//2-r:n//2+r] = initial_u_value
    v[n//2-r:n//2+r, n//2-r:n//2+r] = initial_v_value

    def laplacian(Z):
        return (
            -4*Z +
            np.roll(Z, (0, 1), (0, 1)) +
            np.roll(Z, (0, -1), (0, 1)) +
            np.roll(Z, (1, 0), (0, 1)) +
            np.roll(Z, (-1, 0), (0, 1))
        )

    for _ in range(steps):
        uvv = u * v * v
        du = (D * laplacian(u) - uvv + f * (1 - u))
        dv = (D * laplacian(v) + uvv - (f + k) * v)
        u += du
        v += dv

    return u, v


def generate_plot(u, v, output_file):
    plt.figure()
    plt.imshow(u, cmap='hot')
    plt.colorbar()
    plt.title("Physarum polycephalum Growth")
    plt.savefig(f"{output_file}.png")
    plt.close()


def generate_graphviz_hierarchy(sim: Simulation, output_file):
    dot = graphviz.Digraph(comment='Physarum Hierarchical Structure')
    dot.node('A', 'Physarum polycephalum')
    for i in range(1, 5):
        dot.node(f'B{i}', f'Nucleus {i}')
        dot.edge('A', f'B{i}')
        for j in range(1, 5):
            dot.node(f'C{i}{j}', f'Sub Nucleus {i}{j}')
            dot.edge(f'B{i}', f'C{i}{j}')
    dot.render(output_file, format='png', cleanup=True)


def generate_graphviz_text(sim: Simulation, output_file):
    content = f"""
    digraph G {{
        node [shape=record];
        "Simulation" [label="{{
            Name: {sim.name} |
            Grid Size: {sim.grid_size} |
            Steps: {sim.steps} |
            Diffusion Coefficient: {sim.diffusion_coefficient} |
            Reaction Rate: {sim.reaction_rate} |
            k: {sim.k} |
            Initial U Value: {sim.initial_u_value} |
            Initial V Value: {sim.initial_v_value} |
            Initial Radius: {sim.initial_radius} |
            Conditions: time={sim.conditions['time']}, temperature={sim.conditions['temperature']}, humidity={sim.conditions['humidity']} |
            Outputs: {', '.join(sim.outputs)}
        }}"];
    }}
    """
    with open(f"{output_file}.dot", 'w') as file:
        file.write(content)


# Funkcja generująca graficzną reprezentację grafu
def generate_graphviz_image(output_file):
    dot_file = f"{output_file}.dot"
    graphviz.render('dot', 'png', dot_file)


def parse_yaml_to_simulation(yaml_data: dict) -> Simulation:
    return Simulation(
        name=yaml_data["name"],
        grid_size=yaml_data["grid_size"],
        steps=yaml_data["steps"],
        diffusion_coefficient=yaml_data["diffusion_coefficient"],
        reaction_rate=yaml_data["reaction_rate"],
        k=yaml_data["k"],
        initial_u_value=yaml_data["initial_u_value"],
        initial_v_value=yaml_data["initial_v_value"],
        initial_radius=yaml_data["initial_radius"],
        conditions=yaml_data["conditions"],
        outputs=yaml_data["outputs"]
    )

# Funkcja do wczytywania plików YAML
def load_yaml_from_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Główna funkcja obsługująca folder i pliki YAML
def main():
    parser = argparse.ArgumentParser(description='Run Physarum growth simulations from YAML files.')
    parser.add_argument('--files', type=str, nargs='*', help='The YAML files to process')
    parser.add_argument('--folder', type=str, help='Folder containing YAML files')

    args = parser.parse_args()

    files = args.files if args.files else []
    if args.folder:
        for file_name in os.listdir(args.folder):
            if file_name.endswith('.yaml'):
                files.append(os.path.join(args.folder, file_name))

    if not files:
        print("No YAML files specified.")
        return

    for file in files:
        yaml_data = load_yaml_from_file(file)
        sim = parse_yaml_to_simulation(yaml_data)

        u, v = simulate_reaction_diffusion(sim)

        base_name = os.path.splitext(file)[0]
        generate_plot(u, v, base_name)
        generate_graphviz_text(sim, base_name)
        generate_graphviz_image(base_name)
        generate_graphviz_hierarchy(sim, base_name + '_hierarchy')


if __name__ == "__main__":
    main()