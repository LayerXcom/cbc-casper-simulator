from cbc_casper_simulator.simulator import SimulatorConfig, RandomCreationAndBroadcastSimulator
from cbc_casper_simulator.visualizer import Visualizer
import yaml

yaml_file = "./output/validator.yaml"
graph_file = "output/validator"

simulator = RandomCreationAndBroadcastSimulator(SimulatorConfig.default())
network_states = list(simulator)

result = yaml.dump(network_states[-1].validator_set.all()[0].dump())

with open(yaml_file, 'w') as file:
    file.write(result)

Visualizer.block_store(yaml_file, graph_file)

print("done!")
