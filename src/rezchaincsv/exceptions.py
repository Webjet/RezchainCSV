class MapMissing(Exception):
    def __init__(self, field: str):
        self.field = field


class MapWrong(Exception):
    def __init__(self, key: str, value: str):
        self.field = key
        self.value = value


class ItemWrong(Exception):
    def __init__(self, field: str):
        self.field = field
