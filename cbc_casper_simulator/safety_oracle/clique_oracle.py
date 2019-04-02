from result import Ok, Err, Result
from cbc_casper_simulator.error import *


class CliqueOracle:
    @classmethod
    def check_safety(cls, block, state, validator_set) -> Result[Error, bool]:
        # TODO: implement
        return Ok(True)
