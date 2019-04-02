import yaml
from graphviz import Digraph


class Visualizer:
    @classmethod
    def block_store(cls, validator, output):
        #obj = cls.yml_to_obj(source) if isinstance(source, str) else source

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

        G.render(output)

    @classmethod
    def yml_to_obj(cls, name):
        return yaml.safe_load(open(name))
