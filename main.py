from main.simulation import Simulation
from main.visualizer import Visualizer
import yaml

yaml_file = "./output/validator.yaml"
graph_file = "output/validator"

simulation = Simulation()
validators = simulation.start()
result = yaml.dump(validators.all()[0].dump())

with open(yaml_file, 'w') as file:
    file.write(result)

Visualizer.block_store(yaml_file, graph_file)

