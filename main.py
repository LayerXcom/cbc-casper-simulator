from cbc_casper_simulator.simulator.simulator_config import SimulatorConfig
from cbc_casper_simulator.simulator.random_creation_and_broadcast_simulator import RandomCreationAndBroadcastSimulator
from cbc_casper_simulator.visualizer import Visualizer
import yaml

yaml_file = "./output/output.yaml"

simulator = RandomCreationAndBroadcastSimulator(SimulatorConfig.default())
network_states = list(simulator)
network_state = network_states[-1].dump()

with open(yaml_file, 'w') as file:
    file.write(yaml.dump(network_state))

for validator in network_state["validators"]:
    graph_file = "output/{}".format(validator['name'])
    Visualizer.block_store(validator, graph_file)

print("done!")
