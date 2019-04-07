from cbc_casper_simulator.util.ticker import Ticker


def test_tick():
    ticker = Ticker()
    assert ticker.current() == 0
    ticker.tick()
    assert ticker.current() == 1
