from cbc_casper_simulator.block_proposer import BlockProposer
from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.util.ticker import Ticker


def test_choose():
    ticker: Ticker = Ticker()
    for slot in range(1, 100):
        validators = ValidatorSet.with_equal_weight(slot, ticker).validators
        first = BlockProposer.choose(slot, validators)
        second = BlockProposer.choose(slot, validators)

        # Same proposer is chosen if slot and validators are same
        assert first == second
