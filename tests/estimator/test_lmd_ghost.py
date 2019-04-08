from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.estimator.lmd_ghost_estimator import LMDGhostEstimator


def test_estimate():
    ticker = Ticker()

    v_set = ValidatorSet.with_random_weight(3, ticker)

    messages = dict()
    receiver = v_set.choice_one()
    for sender in v_set.all():
        if sender != receiver:
            m = sender.create_message()
            receiver.add_message(m)
            messages[sender] = m

    justification = receiver.state.justification()
    estimate = LMDGhostEstimator.estimate(receiver.state, justification)

    most_weighted_validator = max(v_set.all(), key=lambda v: v.weight)

    # Most weighted validator's block is chosen as parent.
    assert estimate.parent_hash == messages[most_weighted_validator].estimate.hash


def test_estimate_when_tie_exists():
    ticker = Ticker()

    v_set = ValidatorSet.with_equal_weight(3, ticker)

    messages = dict()
    receiver = v_set.choice_one()
    for sender in v_set.all():
        if sender != receiver:
            m = sender.create_message()
            receiver.add_message(m)
            messages[sender] = m

    justification = receiver.state.justification()
    estimate = LMDGhostEstimator.estimate(receiver.state, justification)

    block_hashes = [m.estimate.hash for m in messages.values()]
    smallest_block_hash = min(block_hashes, key=lambda h: h)

    # The block with the smallest hash is chosen when tie exists.
    assert estimate.parent_hash == smallest_block_hash
