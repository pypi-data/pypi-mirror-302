import argparse
import os
import yaml
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import graphviz


# Definicje struktur danych
class Simulation:
    def __init__(self, name: str, initial_population: float, growth_rate: float, carrying_capacity: float,
                 conditions: Dict, outputs: List[str]):
        self.name = name
        self.initial_population = initial_population
        self.growth_rate = growth_rate
        self.carrying_capacity = carrying_capacity
        self.conditions = conditions
        self.outputs = outputs


# Funkcja do wczytywania plików YAML
def load_yaml_from_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Funkcja do uruchamiania symulacji wzrostu grzybów
def run_simulation(simulation: Simulation):
    time = np.linspace(0, simulation.conditions['time'], 100)  # Generowanie 100 punktów czasowych
    N = simulation.initial_population
    r = simulation.growth_rate
    K = simulation.carrying_capacity

    # Równanie logistyczne: dN/dt = rN(1 - N/K)
    def logistic_growth(t, N):
        return r * N * (1 - N / K)

    # Symulacja wzrostu populacji
    biomass_levels = [N]
    dt = time[1] - time[0]
    for t in time[1:]:
        N = N + logistic_growth(t, N) * dt
        biomass_levels.append(N)

    return time, biomass_levels


# Funkcja generująca wykres wzrostu biomasy
def generate_plot(time, biomass_levels, output_file):
    plt.figure()
    plt.plot(time, biomass_levels, label='Biomass')
    plt.title(f"Biomass Growth Simulation")
    plt.xlabel("Time (days)")
    plt.ylabel("Biomass")
    plt.legend()
    plt.savefig(f"{output_file}.png")
    plt.close()


# Funkcja generująca definicję grafu
def generate_graphviz_text(simulation: Simulation, output_file):
    content = f"""
    digraph G {{
        node [shape=record];
        "Simulation" [label="{{Name: {simulation.name}|Initial Population: {simulation.initial_population}|Growth Rate: {simulation.growth_rate}|Carrying Capacity: {simulation.carrying_capacity}|Conditions: time={simulation.conditions['time']}, temperature={simulation.conditions['temperature']}, humidity={simulation.conditions['humidity']}|Outputs: {', '.join(simulation.outputs)}}}"];
    }}
    """
    with open(f"{output_file}.dot", 'w') as file:
        file.write(content)


# Funkcja generująca graficzną reprezentację grafu
def generate_graphviz_image(output_file):
    dot_file = f"{output_file}.dot"
    graphviz.render('dot', 'png', dot_file)


# Funkcja do tworzenia obiektów symulacji z pliku YAML
def parse_yaml_to_simulation(yaml_data: dict) -> Simulation:
    return Simulation(
        name=yaml_data["name"],
        initial_population=yaml_data["initial_population"],
        growth_rate=yaml_data["growth_rate"],
        carrying_capacity=yaml_data["carrying_capacity"],
        conditions=yaml_data["conditions"],
        outputs=yaml_data["outputs"]
    )


# Główna funkcja
def main():
    parser = argparse.ArgumentParser(description='Run fungal growth simulations from YAML files.')
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
        simulation = parse_yaml_to_simulation(yaml_data)

        time, biomass_levels = run_simulation(simulation)

        base_name = os.path.splitext(file)[0]
        generate_plot(time, biomass_levels, base_name)
        generate_graphviz_text(simulation, base_name)
        generate_graphviz_image(base_name)


if __name__ == "__main__":
    main()