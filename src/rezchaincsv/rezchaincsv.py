import csv
import os
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
        """
        Create and return a Rezchain object.
        map is a dictionary that maps original rezchain terms to field names

        The definitions are as follows
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

        Example of a map in Webbeds:
        SH_MAPPING = {
            'BookingID': rz.COMMON_ID,
            'PartnerName': None,
            'BookingStatus': rz.STATUS,
            'PartnerReference': None,
            'AddedDate': rz.Datetime(null=True),
            'CancelDate': rz.Datetime(null=True),
            'LastChanged': rz.LAST_MODIFIED,
            'checkInDate': rz.CHECKIN,
            'checkOutDate': rz.CHECKOUT,
            'Nights': rz.NIGHTS,
            'NumberofRooms': rz.ROOMS,
            'Currency': rz.CURRENCY,
            'OriginalNetAmount': rz.Number(null=0),
            'CurrentNetAmount': rz.AMOUNT,
        }
        """

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
        # It accepts a dictionary, keys are the names of the fields.
        # Fields not in the mapp are ignored.

        it = {}
        for k, v in item.items():
            if k not in self.types:
                continue
            it[k] = self.types[k].check(v)
        self.items.append(it)
        return it

    def to_csv(self, name: str):
        # Generate a csv file with the specified file name
        with open(name, 'w') as file:
            self.file_to_csv(file)
        return os.path.getsize(file.name)

    def file_to_csv(self, file):
        # Generate a csv file with the specified file object
        writer = csv.DictWriter(file, fieldnames=self.types.keys())
        writer.writeheader()
        for it in self.items:
            writer.writerow(it)

    def to_azure(self, filename: str, share_name: str, conn_string: str, test=False):
        # Upload to the CSV to Azure, you must provide the full filename
        # together with the share name and connection string provided by Rezchain
        # or your Azure administrator

        with tempfile.NamedTemporaryFile() as file:
            self.to_csv(file.name)
            if not test:
                azure_client = ShareFileClient.from_connection_string(
                    conn_str=conn_string,
                    share_name=share_name,
                    file_path=filename
                )
                azure_client.upload_file(file)
                file.seek(0)
            return len(file.read())
