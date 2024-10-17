import json


class ModelhubException(Exception):
    def __init__(self, code: int = 0, msg: str = "", **kwargs):
        self.code = code
        self.msg = msg
        self.context = kwargs

    def __str__(self):
        return json.dumps({"code": self.code, "msg": self.msg})

    __repr__ = __str__
