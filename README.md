# CBC Casper Simulator

[![CircleCI](https://circleci.com/gh/LayerXcom/cbc-casper-simulator.svg?style=svg)](https://circleci.com/gh/LayerXcom/cbc-casper-simulator)

CBC Casper simulator & visualizer

### Mission
Simulator of chain-based consensus protocols to investigate the trade-offs of propeties by changing parameters. 
The target properties are:
- Time to finality
- Message overhead
- TPS

Parameters (or design choices) of protocols are:
- Network latency
- Number of validators
- Fork-choice rule (Longest-chain, GHOST, LMD GHOST, [Prism](https://arxiv.org/pdf/1810.08092.pdf), etc.)
- Vote-by-block vs block-and-vote
- Finality (n confirmation, *finality oracle* in CBC Casper, Casper FFG, etc.)
- Block proposer election (slot-allocation, sortition per slot, etc.)
- Validator rotation
- Adversary


### Requirements
* Python 3.7.2 or later
* Graphviz

### Getting started

CBC Simulator depends on [Graphviz](https://www.graphviz.org/) which is Graph Visualization Software.

You can install Graphviz via Homebrew in macOS.

```
brew install graphviz
```

```
pip install -r requirements.txt
python main.py
```

This will generate `output.yml` by default.
You can specify your simulation parameters file and output file via these options.

```
python main.py -i cbc_casper_simulator/examples/intput.yml -o output.yml
```

For more details, see `spec` directory.

### Run tests

```
pip install -r requirements-test.txt -r requirements.txt
pytest
```
