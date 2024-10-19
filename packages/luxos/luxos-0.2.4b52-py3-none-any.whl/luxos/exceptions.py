import asyncio


class LuxosBaseException(Exception):
    pass


# for all broken messages coming back from miners
class MinerMessageReplyError(LuxosBaseException):
    pass


# messages missing the STATUS/id field
class MinerMessageMalformedError(MinerMessageReplyError):
    pass


# messages with a STATUS = 'E'
class MinerMessageError(MinerMessageReplyError):
    pass


# message reply format invalid
class MinerMessageInvalidError(MinerMessageReplyError):
    pass


class MinerConnectionError(LuxosBaseException):
    def __init__(self, host: str, port: int, *args, **kwargs):
        super().__init__(host, port, *args, **kwargs)
        self.address = (host, port)

    def __str__(self):
        msg = "unknown reason"
        if getattr(self, "__cause__"):
            msg = repr(self.__cause__)
        elif self.args[2:]:
            msg = str(self.args[2])
        return (
            f"<{self.address[0]}:{self.address[1]}>: {self.__class__.__name__}, "
            f"{msg}"
        )


class MinerCommandTimeoutError(MinerConnectionError, asyncio.TimeoutError):
    pass


class MinerCommandSessionAlreadyActive(MinerConnectionError):
    pass


class MinerCommandMalformedMessageError(MinerConnectionError):
    pass


class MinerCommandFailedError(MinerConnectionError):
    pass


class AddressParsingError(LuxosBaseException):
    pass
