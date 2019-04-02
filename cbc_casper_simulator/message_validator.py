from result import Ok, Err, Result
from cbc_casper_simulator.error import MessageValidationError


class MessageValidator:
    @classmethod
    def validate(cls, state, message) -> Result[MessageValidationError, bool]:
        # TOOD: implement
        return Ok(True)
