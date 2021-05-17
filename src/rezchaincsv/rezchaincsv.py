from datetime import date
from collections import OrderedDict
import csv
import numbers
from datetime import datetime, date

from .exceptions import *

DEFAULT_MAPPING = {
    "CommonReferenceID": "Common Reference ID",
    "Amount": "Amount",
    "Currency": "Currency",
    "BookingStatus": "Booking Status",
    "LastModifiedDate": "Last Modified Date",
    "CheckInDate": "Check In Date",
    "CheckOutDate": "Check Out Date",
    "NumberOfNights": "Number Of Nights",
    "NumberOfRooms": "Number Of Rooms",
    "BookingCreationDate": "Booking Creation Date",
    "YourBookingID": "Your Booking ID",
}


class Number():
    def check(self, v):
        if not isinstance(v, numbers.Number):
            raise TypeError(v)
        return float(v)


class Str():
    def check(self, v):
        if not isinstance(v, numbers.Number):
            raise TypeError(v)
        return str(v)


class Datetime():
    def check(self, v):
        if isinstance(v, datetime):
            return v
        raise TypeError(v)


class Date():
    def check(self, v):
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, date):
            return v
        raise TypeError(v)


REQUIRED = {
    "Common Reference ID": Str(),
    "Amount": Number(),
    "Currency": Str(),
    "Booking Status": Str(),
    "Last Modified Date": Datetime(),
}

OPTIONAL = {
    "Check In Date": Date(),
    "Check Out Date": Date(),
    "Number Of Nights": Number(),
    "Number Of Rooms": Number(),
    "Booking Creation Date": Date(),
    "Your Booking ID": Str(),
}


class RezchainItem:
    def __init__(self, map: dict):
        """
        self.CommonReferenceID = CommonReferenceID
        self.Amount = Amount
        self.Currency = Currency
        self.BookingStatus = BookingStatus
        self.LastModifiedDate = LastModifiedDate
        self.CheckInDate = CheckInDate
        self.CheckOutDate = CheckOutDate
        self.NumberOfNights = NumberOfNights
        self.NumberOfRooms = NumberOfRooms
        self.BookingCreationDate = BookingCreationDate
        self.YourBookingID = YourBookingID
        """


class Rezchain:
    def __init__(self, map: dict, prefix: str):
        self.types = {}
        for k in REQUIRED.keys():
            if k not in map:
                raise MapMissing(k)

        for k, v in map.items():
            if k not in REQUIRED and k not in OPTIONAL:
                raise MapWrong(k, v)
            self.types[v] = map[k]

        self.map = map
        self.prefix = prefix
        self.items = []

    def add_item(self, item: dict):
        for k, v in item.items():
            if k != self.types:
                raise ItemWrong(k)
            item[k] = self.types[k](v)
        self.items.append(item)
