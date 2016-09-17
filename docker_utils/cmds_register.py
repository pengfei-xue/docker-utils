class _C:
    """wrap func and helper."""

    def __init__(self, func, h):
        self.func = func
        self.helper = h


class _Commands:
    """commands register."""

    __slots__ = []
    _cmds = {}

    @classmethod
    def register(cls, name, func, helper):
        cls.cmds[name] = _C(func, helper)

    @classmethod
    def all(cls):
        return cls._cmds.keys()
