from cbc_casper_simulator.simulator.simulator_config import SimulatorConfig
from cbc_casper_simulator.simulator.random_creation_and_broadcast_simulator import RandomCreationAndBroadcastSimulator
from cbc_casper_simulator.visualizer import Visualizer
import yaml


def simulate():
    yaml_file = "./output/output.yaml"
    simulator = RandomCreationAndBroadcastSimulator(SimulatorConfig.default())
    states = []
    max_slot = 15

    for slot in range(max_slot):
        network_state = next(simulator)
        network_state_dict = network_state.dump()
        states.append(network_state_dict['validators'][0])

    with open(yaml_file, 'w') as file:
        file.write(yaml.dump(states))
        print("{} was created".format(yaml_file))

    for validator in states:
        graph_file = "output/s{}".format(validator['current_slot'])
        Visualizer.block_store(validator, graph_file)
        print("./{}.png was created.".format(graph_file))

    print("done!")




