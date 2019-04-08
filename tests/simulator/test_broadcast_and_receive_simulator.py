from cbc_casper_simulator.simulator.broadcast_and_receive_simulator import BroadCastAndReceiveSimulator
from cbc_casper_simulator.simulator.config import Config
from cbc_casper_simulator.network.model import Model as NetworkModel


def test_simulate():
    validator_num = 10
    max_slot = 100
    config = Config(validator_num, max_slot)
    simulator = BroadCastAndReceiveSimulator(config)
    for i in range(max_slot):
        model = next(simulator)
        assert isinstance(model, NetworkModel)
