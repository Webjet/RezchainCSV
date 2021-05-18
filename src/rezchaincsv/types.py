import numbers
from datetime import datetime, date


class Number():
    def check(self, v):
        if not isinstance(v, numbers.Number):
            raise TypeError(v)
        return float(v)


class Str():
    def check(self, v):
        return str(v)


class Datetime():
    def check(self, v):
        if isinstance(v, datetime):
            return v.isoformat(sep=' ', timespec='seconds')
        try:
            d = datetime.fromisoformat(v)
            return d.isoformat(sep=' ', timespec='seconds')
        except ValueError:
            raise TypeError(v)


class Date():
    def check(self, v):
        if isinstance(v, datetime):
            return v.date().isoformat()
        if isinstance(v, date):
            return v.isoformat()
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise TypeError(v)
