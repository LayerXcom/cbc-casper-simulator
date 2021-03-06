from cbc_casper_simulator.simulator.config import Config
from cbc_casper_simulator.simulator.broadcast_and_receive_simulator import BroadCastAndReceiveSimulator
from cbc_casper_simulator.estimator.lmd_ghost_estimator import LMDGhostEstimator
import yaml
from graphviz import Digraph


def simulate(render=True):
    yaml_file = "./output/lmd.yaml"
    config = Config.default()
    simulator = BroadCastAndReceiveSimulator(config)

    for i in range(config.max_slot):
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
    visualize_block_score(result, graph_file, render)
    print("{}.png was created.".format(graph_file))


def visualize_block_score(result, output, render):
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

    if render:
        G.render(output)
