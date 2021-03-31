import inspect


class defer_string:
    """"""
    def __init__(self, payload: str) -> None:
        self.payload = payload

    def __str__(self) -> str:
        vars_ = inspect.currentframe().f_back.f_globals.copy()
        vars_.update(inspect.currentframe().f_back.f_locals)
        return self.payload.format(**vars_)
