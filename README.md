# CBC Casper Simulator

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

The result of simulation will be generated in `output` directory by default.
