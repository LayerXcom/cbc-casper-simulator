from cbc_casper_simulator.simulator.config import Config
from cbc_casper_simulator.simulator.broadcast_and_receive_simulator import BroadCastAndReceiveSimulator
import yaml
from graphviz import Digraph


def simulate(render=True):
    yaml_file = "./output/output.yaml"
    simulator = BroadCastAndReceiveSimulator(Config.default())
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
        visualize_validator_state(validator, graph_file, render)
        print("./{}.png was created.".format(graph_file))

    print("done!")


def visualize_validator_state(validator, output, render):
    name = validator["name"]
    slot = validator["current_slot"]
    label = "{}'s view in slot {}".format(name, slot)
    G = Digraph(format='png')
    G.attr(label=label)
    G.attr(fontsize='30')

    messages = validator["state"]["messages"]
    for message in messages:
        h = str(message["hash"])
        sender = message["sender"]
        sender_slot = str(message["sender_slot"])
        receiver_slot = str(message["receiver_slot"])
        label = "Message\n id: {}\n sender: {}\n sender_slot: {}\n receiver_slot: {} ".format(
            h, sender, sender_slot, receiver_slot)
        G.node(h, label)

    # parent-child
    for message in messages:
        child_hash = message["hash"]
        parent_hash = message["parent_hash"]
        if parent_hash is not None:
            G.edge(str(child_hash), str(parent_hash), color='blue')

    # justification
    for message in messages:
        child_hash = str(message["hash"])
        justification = message["justification"]
        for m in justification:
            parent_hash = str(m["message_hash"])
            G.edge(child_hash, parent_hash, color='red')

    if render:
        G.render(output)
