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

COMMON_ID = "Common Reference ID"
AMOUNT = "Amount"
CURRENCY = "Currency"
STATUS = "Booking Status"
LAST_MODIFIED = "Last Modified Date"
CHECKIN = "Check In Date"
CHECKOUT = "Check Out Date"
NIGHTS = "Number Of Nights"
ROOMS = "Number Of Rooms"
CREATION = "Booking Creation Date"
ID = "Your Booking ID"


REQUIRED_FIELDS = {
    COMMON_ID: Str(),
    AMOUNT: Number(),
    CURRENCY: Str(),
    STATUS: Str(),
    LAST_MODIFIED: Datetime(),
}

OPTIONAL_FIELDS = {
    CHECKIN: Date(),
    CHECKOUT: Date(),
    NIGHTS: Number(),
    ROOMS: Number(),
    CREATION: Date(),
    ID: Str(),
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
        mapped = set()
        for k, v in map.items():
            if v is None:
                type = Str()
            elif isinstance(v, RezchainType):
                type = v
            elif v in REQUIRED_FIELDS:
                type = REQUIRED_FIELDS[v]
            elif v in OPTIONAL_FIELDS:
                type = OPTIONAL_FIELDS[v]
            else:
                raise MapWrong(k, v)
            self.types[k] = type
            mapped.add(v)

        for k in REQUIRED_FIELDS.keys():
            if k not in mapped:
                raise MapMissing(k)

        self.map = map
        self.items = []

    def add_item(self, item: dict):
        it = {}
        for k, v in item.items():
            if k not in self.types:
                continue
            it[k] = self.types[k].check(v)
        self.items.append(it)
        return it

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
