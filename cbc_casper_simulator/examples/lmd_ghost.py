from cbc_casper_simulator.simulator.simulator_config import SimulatorConfig
from cbc_casper_simulator.simulator.random_creation_and_broadcast_simulator import RandomCreationAndBroadcastSimulator
from cbc_casper_simulator.estimator.lmd_ghost_estimator import LMDGhostEstimator
import yaml
from graphviz import Digraph


def simulate():
    yaml_file = "./output/lmd.yaml"
    validator_num = 10
    simulator = RandomCreationAndBroadcastSimulator(
        SimulatorConfig(validator_num))

    for i in range(30):
        next(simulator)

    network_state = next(simulator)
    validator = network_state.validator_set.all()[0]

    justification = validator.state.justification()
    state = validator.state
    result = LMDGhostEstimator.dump(state, justification)

    with open(yaml_file, 'w') as file:
        file.write(yaml.dump(result))
        print("{} was created".format(yaml_file))

    graph_file = './output/lmd'
    visualize_block_score(result, graph_file)
    print("{}.png was created.".format(graph_file))


def visualize_block_score(result, output):
    G = Digraph(format='png')
    G.attr(label="score")
    G.attr(fontsize='30')

    latest_message_hashes = [m["message_hash"]
                             for m in result["latest_messages"]]
    messages = result["state"]["messages"]
    for message in messages:
        h = str(message["hash"])
        sender = message["sender"]
        sender_slot = str(message["sender_slot"])
        receiver_slot = str(message["receiver_slot"])
        score = str(message["score"]) if "score" in message else "0"
        label = "Message\n id: {}\n sender: {}\n sender_slot: {}\n receiver_slot: {}\n score: {}".format(
            h, sender, sender_slot, receiver_slot, score)
        if message["hash"] in latest_message_hashes and message["hash"] == result["last_finalized_message"]:
            color = "green"
        elif message["hash"] in latest_message_hashes:
            color = "red"
        elif message["hash"] == result["last_finalized_message"]:
            color = "blue"
        else:
            color = "black"

        G.node(h, label, color=color)

    # parent-child
    for message in messages:
        child_hash = message["hash"]
        parent_hash = message["parent_hash"]
        if parent_hash is not None:
            G.edge(str(child_hash), str(parent_hash), color='blue')

    G.render(output)
