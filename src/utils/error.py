import traceback


class ModManagerException(Exception):
    _msg = "DirNotReady"

    def __init__(self, msg: str | None = None) -> None:
        if msg is not None:
            self._msg = msg

    def get_msg(self) -> str:
        return self._msg

    def trace_back(self):
        print(traceback.format_exc())
        print(self._msg)


class NotValidDirException(ModManagerException):
    _msg = "Not Valid Directory"


class ModNameNotValidException(ModManagerException):
    _msg = "Not Valid Mod Name"


class ModSourceNotReadyException(ModManagerException):
    _msg = "not prepared mod source files"


class NotValidPathException(ModManagerException):
    _msg = "Not Valid Path"


class NotValidSymLinkException(ModManagerException):
    _msg = "Not Valid Symbolic Link"
