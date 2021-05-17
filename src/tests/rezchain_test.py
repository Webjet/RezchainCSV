import unittest
from context import Rezchain, MapMissing
# from rezchaincsv import Rezchain


REQUIRED = {
    "Common Reference ID": "reference_id",
    "Amount": "amount",
    "Currency": "currency",
    "Booking Status": "status",
    "Last Modified Date": "last_modified",
}

OPTIONAL = {
    "Check In Date": "checkin",
    "Check Out Date": "checkout",
    "Number Of Nights": "nights",
    "Number Of Rooms": "rooms",
    "Booking Creation Date": "creation",
    "Your Booking ID": "id",
}


class TestStringMethods(unittest.TestCase):
    def test_required(self):
        rz = Rezchain(REQUIRED, "test")
        self.assertEqual(set(rz.types.keys()), set(REQUIRED.values()))
        # self.assertEqual('foo'.upper(), 'FOO')

    def test_optional(self):
        # rz = Rezchain(OPTIONAL, "test")
        self.assertRaises(MapMissing, Rezchain, OPTIONAL, "test")


if __name__ == '__main__':
    unittest.main()
