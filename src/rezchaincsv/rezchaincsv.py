import csv
import tempfile
from typing import TextIO

# pip3 install azure-storage-file-share
from azure.storage.fileshare import ShareFileClient


from .exceptions import *
from .types import *

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


DATE_FORMAT = ""


REQUIRED_FIELDS = {
    "Common Reference ID": Str(),
    "Amount": Number(),
    "Currency": Str(),
    "Booking Status": Str(),
    "Last Modified Date": Datetime(),
}

OPTIONAL_FIELDS = {
    "Check In Date": Date(),
    "Check Out Date": Date(),
    "Number Of Nights": Number(),
    "Number Of Rooms": Number(),
    "Booking Creation Date": Date(),
    "Your Booking ID": Str(),
}


class Rezchain:
    def __init__(self, map: dict):
        # Create and return a Rezchain object.
        # map is a dictionary that maps original rezchain terms to field names
        #
        # REQUIRED_FIELDS
        # "Common Reference ID": Str(),
        # "Amount": Number(),
        # "Currency": Str(),
        # "Booking Status": Str(),
        # "Last Modified Date": Datetime(),
        #
        # OPTIONAL_FIELDS
        # "Check In Date": Date(),
        # "Check Out Date": Date(),
        # "Number Of Nights": Number(),
        # "Number Of Rooms": Number(),
        # "Booking Creation Date": Date(),
        # "Your Booking ID": Str(),

        self.types = {}
        for k in REQUIRED_FIELDS.keys():
            if k not in map:
                raise MapMissing(k)

        for k, v in map.items():
            which = None
            if k in REQUIRED_FIELDS:
                which = REQUIRED_FIELDS
            elif k in OPTIONAL_FIELDS:
                which = OPTIONAL_FIELDS
            else:
                raise MapWrong(k, v)
            self.types[v] = which[k]

        self.map = map
        self.items = []

    def add_item(self, item: dict):
        for k, v in item.items():
            if k not in self.types:
                raise ItemWrong(k)
            item[k] = self.types[k].check(v)
        self.items.append(item)

    def to_csv(self, name: str):
        with open(name, 'w') as file:
            self.file_to_csv(file)

    def file_to_csv(self, file: TextIO):
        writer = csv.DictWriter(file, fieldnames=self.types.keys())
        writer.writeheader()
        for it in self.items:
            writer.writerow(it)

    def to_azure(self, filename: str, share_name: str, conn_string: str):
        azure_client = ShareFileClient.from_connection_string(
            conn_str=conn_string,
            share_name=share_name,
            file_path=filename
        )

        with tempfile.NamedTemporaryFile(mode='w', newline='') as file:
            self.file_to_csv(file)
            azure_client.upload_file(file)
