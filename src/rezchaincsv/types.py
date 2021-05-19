import numbers
from datetime import datetime, date


class RezchainType:
    def __init__(self, null=False):
        self.null = null
    pass


class Number(RezchainType):
    def check(self, v):
        if not self.null and not isinstance(v, numbers.Number):
            raise ValueError(v)
        if self.null and not v:
            return ''

        try:
            return float(v)
        except ValueError:
            if self.null:
                return ''
            raise ValueError


class Str(RezchainType):
    def check(self, v):
        if self.null and not v:
            return ''
        return str(v)


class Datetime(RezchainType):
    def check(self, v):
        if isinstance(v, datetime):
            return v.isoformat(sep=' ', timespec='minutes')
        try:
            d = datetime.fromisoformat(v)
            return d.isoformat(sep=' ', timespec='minutes')
        except (TypeError, ValueError):
            if self.null:
                return ''
            raise ValueError(v)


class Date(RezchainType):
    def check(self, v):
        if isinstance(v, datetime):
            return v.date().isoformat()
        if isinstance(v, date):
            return v.isoformat()
        try:
            date.fromisoformat(v)
            return v
        except (TypeError, ValueError):
            if self.null:
                return ''
            raise ValueError(v)
